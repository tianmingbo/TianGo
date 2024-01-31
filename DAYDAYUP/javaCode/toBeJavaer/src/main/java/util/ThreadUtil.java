package util;


import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.LockSupport;

public class ThreadUtil {

    /**
     * CPU核数
     **/
    private static final int CPU_COUNT = Runtime.getRuntime().availableProcessors();

    public static void sleepForEver() {

        sleepSeconds(Integer.MAX_VALUE);
    }

    /**
     * 定制的线程工厂
     */
    private static class CustomThreadFactory implements ThreadFactory {
        //线程池数量
        private static final AtomicInteger poolNumber = new AtomicInteger(1);
        private final ThreadGroup group;

        //线程数量
        private final AtomicInteger threadNumber = new AtomicInteger(1);
        private final String threadTag;

        CustomThreadFactory(String threadTag) {
            SecurityManager s = System.getSecurityManager();
            group = (s != null) ? s.getThreadGroup() :
                    Thread.currentThread().getThreadGroup();
            this.threadTag = "apppool-" + poolNumber.getAndIncrement() + "-" + threadTag + "-";
        }

        @Override
        public Thread newThread(Runnable target) {
            Thread t = new Thread(group, target,
                    threadTag + threadNumber.getAndIncrement(),
                    0);
            if (t.isDaemon()) {
                t.setDaemon(false);
            }
            if (t.getPriority() != Thread.NORM_PRIORITY) {
                t.setPriority(Thread.NORM_PRIORITY);
            }
            return t;
        }
    }


    /**
     * 空闲保活时限，单位秒
     */
    private static final int KEEP_ALIVE_SECONDS = 30;
    /**
     * 有界队列size
     */
    private static final int QUEUE_SIZE = 10000;

    /**
     * 核心线程数
     */
    private static final int CORE_POOL_SIZE = 0;
    private static final int MAXIMUM_POOL_SIZE = CPU_COUNT;

    //懒汉式单例创建线程池：用于CPU密集型任务
    private static class CpuIntenseTargetThreadPoolLazyHolder {
        //线程池： 用于CPU密集型任务
        private static final ThreadPoolExecutor EXECUTOR = new ThreadPoolExecutor(
                MAXIMUM_POOL_SIZE,
                MAXIMUM_POOL_SIZE,
                KEEP_ALIVE_SECONDS,
                TimeUnit.SECONDS,
                new LinkedBlockingQueue(QUEUE_SIZE),
                new CustomThreadFactory("cpu"));

        static {
            EXECUTOR.allowCoreThreadTimeOut(true);
            //JVM关闭时的钩子函数
            Runtime.getRuntime().addShutdownHook(
                    new ShutdownHookThread("CPU密集型任务线程池", new Callable<Void>() {
                        @Override
                        public Void call() throws Exception {
                            //优雅关闭线程池
                            shutdownThreadPoolGracefully(EXECUTOR);
                            return null;
                        }
                    }));
        }
    }

    /**
     * IO线程池最大线程数
     */
    private static final int IO_MAX = Math.max(2, CPU_COUNT * 2);
    /**
     * IO线程池核心线程数
     */
    private static final int IO_CORE = 0;

    /**
     * 获取执行CPU密集型任务的线程池
     *
     * @return
     */
    public static ThreadPoolExecutor getCpuIntenseTargetThreadPool() {
        return CpuIntenseTargetThreadPoolLazyHolder.EXECUTOR;
    }

    //懒汉式单例创建线程池：用于IO密集型任务
    private static class IoIntenseTargetThreadPoolLazyHolder {
        //线程池： 用于IO密集型任务
        private static final ThreadPoolExecutor EXECUTOR = new ThreadPoolExecutor(
                IO_MAX,
                IO_MAX,
                KEEP_ALIVE_SECONDS,
                TimeUnit.SECONDS,
                new LinkedBlockingQueue(QUEUE_SIZE),
                new CustomThreadFactory("io"));

        static {
            EXECUTOR.allowCoreThreadTimeOut(true);
            //JVM关闭时的钩子函数
            Runtime.getRuntime().addShutdownHook(
                    new ShutdownHookThread("IO密集型任务线程池", new Callable<Void>() {
                        @Override
                        public Void call() throws Exception {
                            //优雅关闭线程池
                            shutdownThreadPoolGracefully(EXECUTOR);
                            return null;
                        }
                    }));
        }
    }

    static class ShutdownHookThread extends Thread {
        private volatile boolean hasShutdown = false;
        private static AtomicInteger shutdownTimes = new AtomicInteger(0);
        private final Callable callback;

        /**
         * Create the standard hook thread, with a call back, by using {@link Callable} interface.
         *
         * @param name
         * @param callback The call back function.
         */
        public ShutdownHookThread(String name, Callable callback) {
            super("JVM退出钩子(" + name + ")");

            this.callback = callback;
        }

        /**
         * Thread run method.
         * Invoke when the jvm shutdown.
         */
        @Override
        public void run() {
            synchronized (this) {
                System.out.println(getName() + " starting.... ");
                if (!this.hasShutdown) {
                    this.hasShutdown = true;
                    long beginTime = System.currentTimeMillis();
                    try {
                        this.callback.call();
                    } catch (Exception e) {
                        System.out.println(getName() + " error: " + e.getMessage());
                    }
                    long consumingTimeTotal = System.currentTimeMillis() - beginTime;
                    System.out.println(getName() + "  耗时(ms): " + consumingTimeTotal);
                }
            }
        }
    }

    /**
     * 获取执行IO密集型任务的线程池
     *
     * @return
     */
    public static ThreadPoolExecutor getIoIntenseTargetThreadPool() {
        return IoIntenseTargetThreadPoolLazyHolder.EXECUTOR;
    }

    /**
     * 混合线程池
     */
    private static final int MIXED_CORE = 0;  //混合线程池核心线程数
    private static final int MIXED_MAX = 128;  //最大线程数
    private static final String MIXED_THREAD_AMOUNT = "mixed.thread.amount";

    //懒汉式单例创建线程池：用于混合型任务
    private static class MixedTargetThreadPoolLazyHolder {
        //首先从环境变量 mixed.thread.amount 中获取预先配置的线程数
        //如果没有对 mixed.thread.amount 做配置，则使用常量 MIXED_MAX 作为线程数
        private static final int max = (null != System.getProperty(MIXED_THREAD_AMOUNT)) ?
                Integer.parseInt(System.getProperty(MIXED_THREAD_AMOUNT)) : MIXED_MAX;
        //线程池： 用于混合型任务
        private static final ThreadPoolExecutor EXECUTOR = new ThreadPoolExecutor(
                max,
                max,
                KEEP_ALIVE_SECONDS,
                TimeUnit.SECONDS,
                new LinkedBlockingQueue(QUEUE_SIZE),
                new CustomThreadFactory("mixed"));

        static {
            EXECUTOR.allowCoreThreadTimeOut(true);
            //JVM关闭时的钩子函数
            Runtime.getRuntime().addShutdownHook(new ShutdownHookThread("混合型任务线程池", new Callable<Void>() {
                @Override
                public Void call() throws Exception {
                    //优雅关闭线程池
                    shutdownThreadPoolGracefully(EXECUTOR);
                    return null;
                }
            }));
        }
    }

    /**
     * 获取执行混合型任务的线程池     *
     *
     * @return
     */
    public static ThreadPoolExecutor getMixedTargetThreadPool() {
        return MixedTargetThreadPoolLazyHolder.EXECUTOR;
    }

    //懒汉式单例创建线程池：用于定时任务、顺序排队执行任务
    static class SeqOrScheduledTargetThreadPoolLazyHolder {
        //线程池：用于定时任务、顺序排队执行任务
        static final ScheduledThreadPoolExecutor EXECUTOR = new ScheduledThreadPoolExecutor(
                1,
                new CustomThreadFactory("seq"));

        static {
            //JVM关闭时的钩子函数
            Runtime.getRuntime().addShutdownHook(
                    new ShutdownHookThread("定时和顺序任务线程池", new Callable<Void>() {
                        @Override
                        public Void call() throws Exception {
                            //优雅关闭线程池
                            shutdownThreadPoolGracefully(EXECUTOR);
                            return null;
                        }
                    }));
        }

    }


    /**
     * 获取可调度线程池（包含提交延迟、定时、周期性、顺序性执行的任务）
     *
     * @return
     */
    public static ScheduledThreadPoolExecutor getSeqOrScheduledExecutorService() {
        return SeqOrScheduledTargetThreadPoolLazyHolder.EXECUTOR;
    }

    /**
     * 顺序排队执行
     *
     * @param command
     */
    public static void seqExecute(Runnable command) {
        getSeqOrScheduledExecutorService().execute(command);
    }

    /**
     * 延迟执行
     *
     * @param command
     * @param i
     * @param unit
     */
    public static void delayRun(Runnable command, int i, TimeUnit unit) {
        getSeqOrScheduledExecutorService().schedule(command, i, unit);
    }

    /**
     * 固定频率执行
     *
     * @param command
     * @param i
     * @param unit
     */
    public static void scheduleAtFixedRate(Runnable command, int i, TimeUnit unit) {
        getSeqOrScheduledExecutorService().scheduleAtFixedRate(command, i, i, unit);
    }

    /**
     * 线程睡眠
     *
     * @param second 秒
     */
    public static void sleepSeconds(int second) {
        LockSupport.parkNanos(second * 1000L * 1000L * 1000L);
    }

    /**
     * 线程睡眠
     *
     * @param millisecond 毫秒
     */
    public static void sleepMilliSeconds(int millisecond) {
        LockSupport.parkNanos(millisecond * 1000L * 1000L);
    }

    /**
     * 获取当前线程名称
     */
    public static String getCurThreadName() {
        return Thread.currentThread().getName();
    }

    /**
     * 获取当前线程ID
     */
    public static long getCurThreadId() {
        return Thread.currentThread().getId();
    }

    /**
     * 获取当前线程
     */
    public static Thread getCurThread() {
        return Thread.currentThread();
    }

    /**
     * 调用栈中的类名
     *
     * @return
     */
    public static String stackClassName(int level) {
//        Thread.currentThread().getStackTrace()[1]是当前方法 curClassName 执行堆栈
//        Thread.currentThread().getStackTrace()[2]就是 curClassName 的 上一级的方法堆栈 以此类推

        String className = Thread.currentThread().getStackTrace()[level].getClassName();//调用的类名
        return className;

    }

    /**
     * 调用栈中的方法名称
     *
     * @return
     */

    public static String stackMethodName(int level) {
//        Thread.currentThread().getStackTrace()[1]是当前方法 curMethodName 执行堆栈
//        Thread.currentThread().getStackTrace()[2]就是 curMethodName 的 上一级的方法堆栈 以此类推

        String className = Thread.currentThread().getStackTrace()[level].getMethodName();//调用的类名
        return className;
    }

    public static void shutdownThreadPoolGracefully(ExecutorService threadPool) {
        if (!(threadPool instanceof ExecutorService) || threadPool.isTerminated()) {
            return;
        }
        try {
            threadPool.shutdown();   //拒绝接受新任务
        } catch (SecurityException e) {
            return;
        } catch (NullPointerException e) {
            return;
        }
        try {
            // 等待 60 s，等待线程池中的任务完成执行
            if (!threadPool.awaitTermination(60, TimeUnit.SECONDS)) {
                // 调用 shutdownNow 取消正在执行的任务
                threadPool.shutdownNow();
                // 再次等待 60 s，如果还未结束，可以再次尝试，或则直接放弃
                if (!threadPool.awaitTermination(60, TimeUnit.SECONDS)) {
                    System.err.println("线程池任务未正常执行结束");
                }
            }
        } catch (InterruptedException ie) {
            // 捕获异常，重新调用 shutdownNow
            threadPool.shutdownNow();
        }
        //任然没有关闭，循环关闭1000次，每次等待10毫秒
        if (!threadPool.isTerminated()) {
            try {
                for (int i = 0; i < 1000; i++) {
                    if (threadPool.awaitTermination(10, TimeUnit.MILLISECONDS)) {
                        break;
                    }
                    threadPool.shutdownNow();
                }
            } catch (InterruptedException e) {
                System.err.println(e.getMessage());
            } catch (Throwable e) {
                System.err.println(e.getMessage());
            }
        }
    }


}
