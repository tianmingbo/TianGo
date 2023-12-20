package src.main.java.dali.producer;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.HashMap;
import java.util.Properties;

public class CustomProducerParameters {
    /**
     * 生产者提高吞吐量
     */
    public static void main(String[] args) {

        // 0 配置
        Properties prop = new Properties();

        // 连接kafka集群
        prop.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "http://150.158.47.35:9092,http://150.158.47.35:9093,http://150.158.47.35:9094");

        // 序列化
        prop.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        prop.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        // 缓冲区大小,默认32M
        prop.put(ProducerConfig.BUFFER_MEMORY_CONFIG, 33554432);
        // 批次大小 batch.size,默认16k
        prop.put(ProducerConfig.BATCH_SIZE_CONFIG, 16384);

        // linger.ms 等待时间,默认为0, 通常设置为5~100ms
        prop.put(ProducerConfig.LINGER_MS_CONFIG, 1);

        // 压缩
        prop.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "snappy");

        KafkaProducer<String, String> kafkaProducer = new KafkaProducer<>(prop);
        for (int i = 0; i < 5; i++) {
            kafkaProducer.send(new ProducerRecord<>("tiandali", "test" + i));
        }
        kafkaProducer.close();
    }
}
