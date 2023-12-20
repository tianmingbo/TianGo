package src.main.java.dali.producer;

import org.apache.kafka.clients.producer.Partitioner;
import org.apache.kafka.common.Cluster;
import org.apache.kafka.common.PartitionInfo;

import java.util.List;
import java.util.Map;

/**
 * 自定义分区器
 *
 * @author tianmingbo
 */
public class MyPartitioner implements Partitioner {
    /**
     * 计算给定消息要被发送到哪个分区
     *
     * @param topic      topic 名称
     * @param keyObj        消息键值或 null
     * @param keyBytes   消息键值序列化字节数组或 null
     * @param valueObj      消息体或 null
     * @param valueBytes 消息体序列化字节数组或 null
     * @param cluster    集群元数据
     */
    @Override
    public int partition(String topic, Object keyObj, byte[] keyBytes, Object valueObj, byte[] valueBytes, Cluster cluster) {
        String value = (String) valueObj;
        List<PartitionInfo> partitionInfoList = cluster.availablePartitionsForTopic(topic);
        int size = partitionInfoList.size();
        String s = value.substring(value.length() - 1);
        try {
            int i = Integer.parseInt(s);
            return i % 5 == 0 ? 0 : size - 1;
        } catch (Exception e) {
            return 0;
        }
    }

    @Override
    public void close() {

    }

    @Override
    public void configure(Map<String, ?> configs) {

    }
}
