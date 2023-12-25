package src.main.consumer;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Properties;
import java.util.Set;

public class CustomConsumerSeek {

    public static void main(String[] args) {

        // 0 配置信息
        Properties prop = new Properties();

        // 连接
        prop.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,"hadoop102:9092,hadoop103:9092");

        // 反序列化
        prop.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        prop.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());

        // 组id
        prop.put(ConsumerConfig.GROUP_ID_CONFIG,"test3");

        // 1 创建消费者
        KafkaConsumer<String, String> kafkaConsumer = new KafkaConsumer<>(prop);

        // 2 订阅主题
        ArrayList<String> topics = new ArrayList<>();
        topics.add("tiandali");
        kafkaConsumer.subscribe(topics);

        // 指定位置进行消费
        Set<TopicPartition> assignment = kafkaConsumer.assignment();

        //  保证分区分配方案已经制定完毕
        while (assignment.size() == 0){
            kafkaConsumer.poll(Duration.ofSeconds(1));

            assignment = kafkaConsumer.assignment();
        }

        // 指定消费的offset
        for (TopicPartition topicPartition : assignment) {
            kafkaConsumer.seek(topicPartition,600);
        }

        // 3  消费数据
        while (true){

            ConsumerRecords<String, String> consumerRecords = kafkaConsumer.poll(Duration.ofSeconds(1));

            for (ConsumerRecord<String, String> consumerRecord : consumerRecords) {

                System.out.println(consumerRecord);
            }
        }
    }
}
