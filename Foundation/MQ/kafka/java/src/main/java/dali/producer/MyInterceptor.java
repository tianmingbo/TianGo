package src.main.java.dali.producer;

import org.apache.kafka.clients.producer.ProducerInterceptor;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.util.Map;

/**
 * @author tianmingbo
 */
public class MyInterceptor implements ProducerInterceptor<String, String> {
    private int errorCounter = 0;
    private int successCounter = 0;

    @Override
    public ProducerRecord onSend(ProducerRecord record) {
        //把时间戳写入消息体的最前部
        return new ProducerRecord(
                record.topic(), record.partition(), record.timestamp(),
                record.key(), System.currentTimeMillis() + "," + record.value().toString());
    }


    @Override
    public void onAcknowledgement(RecordMetadata metadata, Exception exception) {
        //统计成功失败数量
        if (exception == null) {
            successCounter++;
        } else {
            errorCounter++;
        }
    }

    @Override
    public void close() {
        // 保存结果
        System.out.println("Successful sent: " + successCounter);
        System.out.println("Failed sent: " + errorCounter);
    }

    @Override
    public void configure(Map<String, ?> configs) {

    }
}
