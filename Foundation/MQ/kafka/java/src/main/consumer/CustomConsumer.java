package src.main.consumer;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Properties;

/**
 * @author tianmingbo
 */
public class CustomConsumer {

    public static void main(String[] args) {

        // 0 配置
        Properties prop = new Properties();

        // 连接 bootstrap.servers
        prop.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "http://150.158.47.35:9092,http://150.158.47.35:9093,http://150.158.47.35:9094");

        // 反序列化
        prop.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
//        prop.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        prop.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "src.main.consumer.MyDeserializer");

        // 配置消费者组id
        prop.put(ConsumerConfig.GROUP_ID_CONFIG, "test");
        prop.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        // 设置分区分配策略
        prop.put(ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG, "org.apache.kafka.clients.consumer.StickyAssignor");

        // 1 创建一个消费者  "", "hello"
        KafkaConsumer<String, String> kafkaConsumer = new KafkaConsumer<>(prop);

        // 2 订阅主题 tiandali
        ArrayList<String> topics = new ArrayList<>();
        topics.add("tiandali");
        kafkaConsumer.subscribe(topics);

        // 3 消费数据
        while (true) {

            ConsumerRecords<String, String> consumerRecords = kafkaConsumer.poll(Duration.ofSeconds(1));

            for (ConsumerRecord<String, String> consumerRecord : consumerRecords) {
                System.out.println(consumerRecord);
            }

            kafkaConsumer.commitAsync();
        }
    }
}
