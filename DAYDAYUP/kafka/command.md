## 命令行
#### 1、kafka-topics.sh --list --bootstrap-server kafka1:9092  #列出已创建的主题
#### 2、kafka-topics.sh --create --bootstrap-server kafka1:9092 --topic  test_hello_world --partitions 3 --replication-factor 3 #创建分区
```
--partitions 决定了主题将分为多少个分区；
--replication-factor 表示每个分区有3个副本
--bootstrap-server 指向broker
```
#### 3、kafka-console-producer.sh  --bootstrap-server kafka01:9092 --topic TestComposeTopi #启动一个控制台生产者
#### 4、kafka-console-consumer.sh --bootstrap-server kafka01:9092 --topic TestComposeTopic --from-beginning #启动一个控制台消费者
#### 5、kafka-consumer-groups.sh --bootstrap-server 10.8.169.156:9092 --describe  --all-groups |grep CCS-Harbour-Vehicle-grantedArea  #查看消费组
#### 6、./kafka-consumer-groups.sh --bootstrap-server localhost:9092 --delete --group my-group #删除消费组
