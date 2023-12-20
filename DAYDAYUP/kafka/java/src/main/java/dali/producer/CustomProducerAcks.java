package src.main.java.dali.producer;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

/**
 * @author tianmingbo
 */
public class CustomProducerAcks {
    /**
     * 数据完全可靠条件 = ACK级别设置为-1 + 分区副本大于等于2 + ISR里应答的最小副本数量大于等于2
     */
    public static void main(String[] args) {

        // 0 配置
        Properties prop = new Properties();

        // 连接集群 bootstrap.servers
        prop.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "http://150.158.47.35:9092,http://150.158.47.35:9093,http://150.158.47.35:9094");

        // 指定对应的key和value的序列化类型 key.serializer
        prop.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        prop.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // acks
        prop.put(ProducerConfig.ACKS_CONFIG, "1");

        // 重试次数,默认是 int 最大值， 2147483647
        prop.put(ProducerConfig.RETRIES_CONFIG, 3);

        KafkaProducer<String, String> kafkaProducer = new KafkaProducer<>(prop);
        for (int i = 0; i < 5; i++) {
            kafkaProducer.send(new ProducerRecord<>("tiandali", "test" + i));
        }
        kafkaProducer.close();
    }
}
