package src.main.java.dali.producer;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;
import java.util.concurrent.ExecutionException;

/**
 * 同步发送
 * @author tianmingbo
 */
public class ProducerSync {

    public static void main(String[] args) throws ExecutionException, InterruptedException {

        // 0 配置
        Properties prop = new Properties();

        // 连接集群 bootstrap.servers
        prop.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "http://150.158.47.35:9092,http://150.158.47.35:9093,http://150.158.47.35:9094");

        // 指定对应的key和value的序列化类型 key.serializer
        prop.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        prop.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // 1 创建kafka生产者对象
        KafkaProducer<String, String> kafkaProducer = new KafkaProducer<>(prop);

        // 2 发送数据
        for (int i = 0; i < 5; i++) {
            //同步，发送成功后才继续发送下一条
            kafkaProducer.send(new ProducerRecord<>("tiandali", "test" + i)).get();
        }

        // 3 关闭资源
        kafkaProducer.close();
    }
}
