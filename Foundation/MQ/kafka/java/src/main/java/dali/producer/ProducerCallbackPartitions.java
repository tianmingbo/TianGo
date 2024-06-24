package src.main.java.dali.producer;

import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

/**
 * 指定分区
 *
 * @author tianmingbo
 */
public class ProducerCallbackPartitions {

    public static void main(String[] args) throws InterruptedException {

        // 0 配置
        Properties prop = new Properties();

        // 连接集群 bootstrap.servers
        prop.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "http://150.158.47.35:9092,http://150.158.47.35:9093,http://150.158.47.35:9094");


        // 指定对应的key和value的序列化类型 key.serializer
        prop.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        prop.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // 关联自定义分区器
        prop.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, "src.main.java.dali.producer.MyPartitioner");

        // 1 创建kafka生产者对象
        KafkaProducer<String, String> kafkaProducer = new KafkaProducer<>(prop);

        // 2 发送数据
        for (int i = 0; i < 500; i++) {
            //指定分区
            kafkaProducer.send(new ProducerRecord<>("tiandali", "hello" + i), (metadata, exception) -> {
                if (exception == null) {
                    System.out.println("主题： " + metadata.topic() + " 分区： " + metadata.partition());
                }
            });

            Thread.sleep(2);
        }

        // 3 关闭资源
        kafkaProducer.close();
    }
}
