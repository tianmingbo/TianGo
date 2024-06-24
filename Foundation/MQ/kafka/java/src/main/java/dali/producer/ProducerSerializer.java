package src.main.java.dali.producer;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;


/**
 * @author tianmingbo
 * 自定义序列化类
 */
public class ProducerSerializer {
    public static void main(String[] args) {
        Properties prop = new Properties();
        prop.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "http://150.158.47.35:9092,http://150.158.47.35:9093,http://150.158.47.35:9094");

        prop.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        prop.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, MySerializer.class.getName());
        Person person = new Person("dali", 18);
        KafkaProducer<String, Person> producer = new KafkaProducer<>(prop);

        for (int i = 0; i < 10; i++) {
            producer.send(new ProducerRecord<>("tiandali", person));
        }
        producer.close();
    }
}
