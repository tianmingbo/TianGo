import json
import logging
from abc import abstractmethod
from pathlib import Path
from typing import Optional, Type, TypeVar

from twisted.internet.defer import Deferred

from scrapy.crawler import Crawler
from scrapy.http.request import Request
from scrapy.spiders import Spider
from scrapy.utils.job import job_dir
from scrapy.utils.misc import create_instance, load_object

logger = logging.getLogger(__name__)


class BaseSchedulerMeta(type):
    """
    Metaclass to check scheduler classes against the necessary interface
    """

    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (
                hasattr(subclass, "has_pending_requests")
                and callable(subclass.has_pending_requests)
                and hasattr(subclass, "enqueue_request")
                and callable(subclass.enqueue_request)
                and hasattr(subclass, "next_request")
                and callable(subclass.next_request)
        )


class BaseScheduler(metaclass=BaseSchedulerMeta):
    """
    The scheduler component is responsible for storing requests received from
    the engine, and feeding them back upon request (also to the engine).

    The original sources of said requests are:

    * Spider: ``start_requests`` method, requests created for URLs in the ``start_urls`` attribute, request callbacks
    * Spider middleware: ``process_spider_output`` and ``process_spider_exception`` methods
    * Downloader middleware: ``process_request``, ``process_response`` and ``process_exception`` methods

    The order in which the scheduler returns its stored requests (via the ``next_request`` method)
    plays a great part in determining the order in which those requests are downloaded.

    The methods defined in this class constitute the minimal interface that the Scrapy engine will interact with.
    """

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """
        Factory method which receives the current :class:`~scrapy.crawler.Crawler` object as argument.
        """
        return cls()

    def open(self, spider: Spider) -> Optional[Deferred]:
        """
        Called when the spider is opened by the engine. It receives the spider
        instance as argument and it's useful to execute initialization code.

        :param spider: the spider object for the current crawl
        :type spider: :class:`~scrapy.spiders.Spider`
        """
        pass

    def close(self, reason: str) -> Optional[Deferred]:
        """
        Called when the spider is closed by the engine. It receives the reason why the crawl
        finished as argument and it's useful to execute cleaning code.

        :param reason: a string which describes the reason why the spider was closed
        :type reason: :class:`str`
        """
        pass

    @abstractmethod
    def has_pending_requests(self) -> bool:
        """
        ``True`` if the scheduler has enqueued requests, ``False`` otherwise
        """
        raise NotImplementedError()

    @abstractmethod
    def enqueue_request(self, request: Request) -> bool:
        """
        Process a request received by the engine.

        Return ``True`` if the request is stored correctly, ``False`` otherwise.

        If ``False``, the engine will fire a ``request_dropped`` signal, and
        will not make further attempts to schedule the request at a later time.
        For reference, the default Scrapy scheduler returns ``False`` when the
        request is rejected by the dupefilter.
        """
        raise NotImplementedError()

    @abstractmethod
    def next_request(self) -> Optional[Request]:
        """
        Return the next :class:`~scrapy.http.Request` to be processed, or ``None``
        to indicate that there are no requests to be considered ready at the moment.

        Returning ``None`` implies that no request from the scheduler will be sent
        to the downloader in the current reactor cycle. The engine will continue
        calling ``next_request`` until ``has_pending_requests`` is ``False``.
        """
        raise NotImplementedError()


SchedulerTV = TypeVar("SchedulerTV", bound="Scheduler")


class Scheduler(BaseScheduler):
    """
    默认的 Scrapy 调度器。 此实现还处理重复url
     通过 :settings中的:`dupefilter <DUPEFILTER_CLASS>` 过滤。

     该调度程序将请求存储到多个优先级队列（由
     :setting:`SCHEDULER_PRIORITY_QUEUE` 设置）。 依次表示优先队列
     由基于内存或磁盘的队列支持（分别由
     :setting:`SCHEDULER_MEMORY_QUEUE` 和 :setting:`SCHEDULER_DISK_QUEUE` 设置)。

    请求优先级几乎完全委托给优先级队列。 此调度程序执行的唯一优先级排序是使用基于磁盘的队列（如果存在）
    （即如果定义了 JOBDIR 设置）并在发生序列化错误时回退到基于内存的队列。 如果磁盘队列不存在，则直接使用内存队列。

     :param dupefilter: 负责检查和过滤重复请求的对象。
                        默认使用 DUPEFILTER_CLASS 设置的值。
     :type dupefilter: :class:`scrapy.dupefilters.BaseDupeFilter` 实例或类似的：
                       任何实现 `BaseDupeFilter` 接口的类

     :param jobdir: 用于保存爬虫状态的目录路径。
                    默认情况下使用 :setting:`JOBDIR` 设置的值。
                    请参阅：ref：`topics-jobs`。
     :type jobdir: :class:`str` 或 ``None``

     ：param dqclass：用作持久请求队列的类。
                     默认情况下使用 :setting:`SCHEDULER_DISK_QUEUE` 设置的值。
     :type dqclass: 类

     ：param mqclass：用作非持久请求队列的类。
                     默认情况下使用 :setting:`SCHEDULER_MEMORY_QUEUE` 设置的值。
     :type mqclass: 类

     ：param logunser：一个布尔值，指示是否应记录不可序列化的请求。
                      默认情况下使用 :setting:`SCHEDULER_DEBUG` 设置的值。
     :type logunser: bool

     :param stats: 一个统计收集器对象，用于记录有关请求调度过程的统计信息。
                   默认情况下使用 :setting:`STATS_CLASS` 设置的值。
     :type stats: :class:`scrapy.statscollectors.StatsCollector` 实例或类似的：
                  任何实现“StatsCollector”接口的类

     :param pqclass: 用作请求优先级队列的类。
                     默认情况下使用 :setting:`SCHEDULER_PRIORITY_QUEUE` 设置的值。
     :type pqclass: 类

     :param crawler: 当前爬取对应的爬虫对象。
     ：类型爬虫：：类：`scrapy.crawler.Crawler`
    """

    def __init__(
            self,
            dupefilter,
            jobdir: Optional[str] = None,
            dqclass=None,
            mqclass=None,
            logunser: bool = False,
            stats=None,
            pqclass=None,
            crawler: Optional[Crawler] = None,
    ):
        self.df = dupefilter  # 指纹过滤器
        self.dqdir = self._dqdir(jobdir)  # 任务队列文件夹
        self.pqclass = pqclass  # 优先级任务队列类
        self.dqclass = dqclass  # 磁盘任务队列类
        self.mqclass = mqclass  # 内存任务队列类
        self.logunser = logunser  # 日志是否序列化
        self.stats = stats
        self.crawler = crawler

    @classmethod
    def from_crawler(cls: Type[SchedulerTV], crawler) -> SchedulerTV:
        """
        Factory method, initializes the scheduler with arguments taken from the crawl settings
        """
        dupefilter_cls = load_object(crawler.settings["DUPEFILTER_CLASS"])  # 从配置文件中获取指纹过滤器类
        # 从配置文件中依次获取优先级任务队列类、磁盘队列类、内存队列类
        return cls(
            dupefilter=create_instance(dupefilter_cls, crawler.settings, crawler),
            jobdir=job_dir(crawler.settings),
            dqclass=load_object(crawler.settings["SCHEDULER_DISK_QUEUE"]),
            mqclass=load_object(crawler.settings["SCHEDULER_MEMORY_QUEUE"]),
            logunser=crawler.settings.getbool("SCHEDULER_DEBUG"),
            stats=crawler.stats,
            pqclass=load_object(crawler.settings["SCHEDULER_PRIORITY_QUEUE"]),
            crawler=crawler,
        )

    def has_pending_requests(self) -> bool:
        return len(self) > 0

    def open(self, spider: Spider) -> Optional[Deferred]:
        """
        (1) initialize the memory queue
        (2) initialize the disk queue if the ``jobdir`` attribute is a valid directory
        (3) return the result of the dupefilter's ``open`` method
        """
        self.spider = spider
        self.mqs = self._mq()  # 实例化优先级队列
        self.dqs = self._dq() if self.dqdir else None  # 如果定义了dqdir则实例化基于磁盘的队列
        return self.df.open()  # 调用请求指纹过滤器的open方法

    def close(self, reason: str) -> Optional[Deferred]:
        """
        (1) dump pending requests to disk if there is a disk queue
        (2) return the result of the dupefilter's ``close`` method
        """
        if self.dqs is not None:
            state = self.dqs.close()
            assert isinstance(self.dqdir, str)
            self._write_dqs_state(self.dqdir, state)
        return self.df.close(reason)

    def enqueue_request(self, request: Request) -> bool:
        """
        Unless the received request is filtered out by the Dupefilter, attempt to push
        it into the disk queue, falling back to pushing it into the memory queue.

        Increment the appropriate stats, such as: ``scheduler/enqueued``,
        ``scheduler/enqueued/disk``, ``scheduler/enqueued/memory``.

        Return ``True`` if the request was stored successfully, ``False`` otherwise.
        """
        # 请求入队 若请求过滤器验证重复 返回False
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        # 磁盘队列是否入队成功
        dqok = self._dqpush(request)
        if dqok:
            self.stats.inc_value("scheduler/enqueued/disk", spider=self.spider)
        else:
            # 没有定义磁盘队列 则使用内存队列
            self._mqpush(request)
            self.stats.inc_value("scheduler/enqueued/memory", spider=self.spider)
        self.stats.inc_value("scheduler/enqueued", spider=self.spider)
        return True

    def next_request(self) -> Optional[Request]:
        """
        Return a :class:`~scrapy.http.Request` object from the memory queue,
        falling back to the disk queue if the memory queue is empty.
        Return ``None`` if there are no more enqueued requests.

        Increment the appropriate stats, such as: ``scheduler/dequeued``,
        ``scheduler/dequeued/disk``, ``scheduler/dequeued/memory``.
        """
        request = self.mqs.pop()
        if request is not None:
            self.stats.inc_value("scheduler/dequeued/memory", spider=self.spider)
        else:
            request = self._dqpop()
            if request is not None:
                self.stats.inc_value("scheduler/dequeued/disk", spider=self.spider)
        if request is not None:
            self.stats.inc_value("scheduler/dequeued", spider=self.spider)
        return request

    def __len__(self) -> int:
        """
        Return the total amount of enqueued requests
        """
        return len(self.dqs) + len(self.mqs) if self.dqs is not None else len(self.mqs)

    def _dqpush(self, request: Request) -> bool:
        # 是否定义磁盘队列
        if self.dqs is None:
            return False
        try:
            # 放入磁盘队列
            self.dqs.push(request)
        except ValueError as e:  # non serializable request
            if self.logunser:
                msg = (
                    "Unable to serialize request: %(request)s - reason:"
                    " %(reason)s - no more unserializable requests will be"
                    " logged (stats being collected)"
                )
                logger.warning(
                    msg,
                    {"request": request, "reason": e},
                    exc_info=True,
                    extra={"spider": self.spider},
                )
                self.logunser = False
            self.stats.inc_value("scheduler/unserializable", spider=self.spider)
            return False
        else:
            return True

    def _mqpush(self, request: Request) -> None:
        # 入内存队列
        self.mqs.push(request)

    def _dqpop(self) -> Optional[Request]:
        if self.dqs is not None:
            return self.dqs.pop()
        return None

    def _mq(self):
        """Create a new priority queue instance, with in-memory storage"""
        return create_instance(
            self.pqclass,
            settings=None,
            crawler=self.crawler,
            downstream_queue_cls=self.mqclass,
            key="",
        )

    def _dq(self):
        """Create a new priority queue instance, with disk storage"""
        state = self._read_dqs_state(self.dqdir)
        q = create_instance(
            self.pqclass,
            settings=None,
            crawler=self.crawler,
            downstream_queue_cls=self.dqclass,
            key=self.dqdir,
            startprios=state,
        )
        if q:
            logger.info(
                "Resuming crawl (%(queuesize)d requests scheduled)",
                {"queuesize": len(q)},
                extra={"spider": self.spider},
            )
        return q

    def _dqdir(self, jobdir: Optional[str]) -> Optional[str]:
        """Return a folder name to keep disk queue state at"""
        if jobdir is not None:
            dqdir = Path(jobdir, "requests.queue")
            if not dqdir.exists():
                dqdir.mkdir(parents=True)
            return str(dqdir)
        return None

    def _read_dqs_state(self, dqdir: str) -> list:
        path = Path(dqdir, "active.json")
        if not path.exists():
            return []
        with path.open(encoding="utf-8") as f:
            return json.load(f)

    def _write_dqs_state(self, dqdir: str, state: list) -> None:
        with Path(dqdir, "active.json").open("w", encoding="utf-8") as f:
            json.dump(state, f)
