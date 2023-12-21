package src.main.java.dali.producer;

import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.errors.RetriableException;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

/**
 * 异步发送
 *
 * @author tianmingbo
 */
public class ProducerCallback {

    public static void main(String[] args) throws InterruptedException {

        // 0 配置
        Properties prop = new Properties();

        // 连接集群 bootstrap.servers
        prop.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "http://150.158.47.35:9092,http://150.158.47.35:9093,http://150.158.47.35:9094");


        // 指定对应的key和value的序列化类型 key.serializer
//        prop.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringSerializer");
        prop.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        prop.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // 1 创建kafka生产者对象
        // "" hello
        KafkaProducer<String, String> kafkaProducer = new KafkaProducer<>(prop);
        // 2 发送数据
        for (int i = 0; i < 500; i++) {
            kafkaProducer.send(new ProducerRecord<>("tiandali", "test" + i), (metadata, exception) -> {
                if (exception == null) {
                    System.out.println("主题： " + metadata.topic() + " 分区： " + metadata.partition());
                } else {
                    if (exception instanceof RetriableException) {
                        System.out.println("retry error");
                    } else {
                        System.out.println("real error");
                    }
                }
            });

            Thread.sleep(2);
        }

        // 3 关闭资源
        kafkaProducer.close();
    }
}
