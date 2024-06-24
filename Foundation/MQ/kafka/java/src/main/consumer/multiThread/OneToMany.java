package src.main.consumer.multiThread;

import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.errors.WakeupException;
import org.apache.kafka.common.serialization.ByteBufferDeserializer;

import java.util.*;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

//consumer 多线程管理类，用于创建线程池以及为每个线程分配消息集合。另外 consumer 位移提交也在该类中完成
class ConsumerThreadHandler<K, V> {
    private final KafkaConsumer<K, V> consumer;
    private ExecutorService executors;
    private final Map<TopicPartition, OffsetAndMetadata> offsets = new HashMap<>();

    public ConsumerThreadHandler(String brokerList, String groupId, String topic) {
        Properties props = new Properties();
        props.put("bootstrap.servers", brokerList);//必须指定
        props.put("group.id", groupId);//必须指定
        props.put("enable.auto.commit", "false");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put("key.deserializer", ByteBufferDeserializer.class.getName());
        props.put("value.deserializer", ByteBufferDeserializer.class.getName());
        consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Arrays.asList(topic), new ConsumerRebalanceListener() {
            @Override
            public void onPartitionsRevoked(Collection<TopicPartition> partitions) {
                consumer.commitSync(offsets);//提交位移
            }

            @Override
            public void onPartitionsAssigned(Collection<TopicPartition> partitions) {
                offsets.clear();
            }
        });
    }

    /**
     * 消费主方法
     *
     * @param threadNumber 线程池中的线程数
     */
    public void consume(int threadNumber) {
        executors = new ThreadPoolExecutor(threadNumber, threadNumber, 0L, TimeUnit.MILLISECONDS, new ArrayBlockingQueue<Runnable>(1000), new ThreadPoolExecutor.CallerRunsPolicy());
        try {
            while (true) {
                ConsumerRecords<K, V> records = consumer.poll(1000L);
                if (!records.isEmpty()) {
                    executors.submit(new ConsumerWorker<>(records, offsets));
                }
                commitOffsets();
            }
        } catch (WakeupException e) {
            //此处忽略此异常的处理
        } finally {
            commitOffsets();
            consumer.close();
        }
    }

    private void commitOffsets() {
        // 尽量降低 synchronized 块对 offsets 锁定的时间
        Map<TopicPartition, OffsetAndMetadata> unmodfiedMap;
        synchronized (offsets) {
            if (offsets.isEmpty()) {
                return;
            }
            unmodfiedMap = Collections.unmodifiableMap(new HashMap<>(offsets));
            offsets.clear();
        }
        consumer.commitSync(unmodfiedMap);
    }

    public void close() {
        consumer.wakeup();
        executors.shutdown();
    }
}

//执行真正的消费逻辑并上报位移信息给ConsumerThreadHandler
class ConsumerWorker<K, V> implements Runnable {
    private final ConsumerRecords<K, V> records;
    private final Map<TopicPartition, OffsetAndMetadata> offsets;

    public ConsumerWorker(ConsumerRecords<K, V> record, Map<TopicPartition, OffsetAndMetadata> offsets) {
        this.records = record;
        this.offsets = offsets;
    }

    @Override
    public void run() {
        for (TopicPartition partition : records.partitions()) {
            List<ConsumerRecord<K, V>> partitionRecords = records.records(partition);
            for (ConsumerRecord<K, V> record : partitionRecords) {
                System.out.printf("topic=%s, partition=%d, offset = % d%n", record.topic(), record.partition(), record.offset());
            }
            // 上报位移信息
            long lastOffset = partitionRecords.get(partitionRecords.size() - 1).offset();
            synchronized (offsets) {
                if (!offsets.containsKey(partition)) {
                    offsets.put(partition, new OffsetAndMetadata(lastOffset + 1));
                } else {
                    long curr = offsets.get(partition).offset();
                    if (curr <= lastOffset + 1) {
                        offsets.put(partition, new OffsetAndMetadata(lastOffset + 1));
                    }
                }
            }
        }
    }
}

/**
 * @author tianmingbo
 * 单 KafkaConsumer 实例+多 worker 线程
 * 将消息的获取与消息的处理解耦，把后者放入单独的工作者线程中，即所谓的 worker 线程中。
 * 同时在全局维护一个或若干个 consumer 实例执行消息获取任务
 */
public class OneToMany {
    public static void main(String[] args) {
        String brokerList = "localhost:9092";
        String topic = "test-topic";
        String groupID = "test-group";
        final ConsumerThreadHandler<byte[], byte[]> handler = new ConsumerThreadHandler<>(brokerList, groupID, topic);
        final int cpuCount = Runtime.getRuntime().availableProcessors();
        Runnable runnable = () -> handler.consume(cpuCount);
        new Thread(runnable).start();
        try {
            // 20 秒后自动停止该测试程序
            Thread.sleep(20000L);
        } catch (InterruptedException e) {
            // 此处忽略此异常的处理
        }
        System.out.println("Starting to close the consumer...");
        handler.close();
    }
}

