package src.main.consumer;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Properties;

public class CustomConsumerAutoOffset {

    public static void main(String[] args) {

        // 0 配置
        Properties prop = new Properties();

        // 连接 bootstrap.servers
        prop.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "hadoop102:9092,hadoop103:9092");

        // 反序列化
        prop.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        prop.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());

        // 配置消费者组id
        prop.put(ConsumerConfig.GROUP_ID_CONFIG, "test");

        // 手动提交
        prop.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);


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
            kafkaConsumer.commitAsync(); //异步提交
//            kafkaConsumer.commitSync();
        }
    }
}
