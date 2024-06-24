package src.main.java.dali.producer;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.ArrayList;
import java.util.Properties;

/**
 * @author tianmingbo
 * 自定义拦截器
 */
public class ProducerInterceptorDemo {
    public static void main(String[] args) {
        Properties prop = new Properties();
        prop.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "http://150.158.47.35:9092,http://150.158.47.35:9093,http://150.158.47.35:9094");

        prop.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        prop.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        ArrayList<String> interceptors = new ArrayList<>();
        interceptors.add("src.main.java.dali.producer.MyInterceptor");
        prop.put(ProducerConfig.INTERCEPTOR_CLASSES_CONFIG, interceptors);
        KafkaProducer<String, String> producer = new KafkaProducer<>(prop);

        // 2 发送数据
        for (int i = 0; i < 5; i++) {
            //构建消息实例
            producer.send(new ProducerRecord<>("tiandali", "dali" + i));
        }

        // 3 关闭资源*** 别忘喽释放资源
        producer.close();
    }
}
