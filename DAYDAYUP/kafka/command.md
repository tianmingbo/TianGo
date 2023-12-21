## 命令

### 列出已创建的主题

```shell
kafka-topics.sh --list --bootstrap-server kafka1:9092
```

### 创建分区

```sh
- kafka-topics.sh --create --bootstrap-server kafka1:9092 --topic  test_hello_world --partitions 3 --replication-factor 3 
- > --partitions 决定了主题将分为多少个分区；
  > --replication-factor 表示每个分区有3个副本
  > --bootstrap-server 指向broker
```

### 启动一个控制台生产者

```sh
kafka-console-producer.sh  --bootstrap-server kafka01:9092 --topic TestComposeTopi
```

### 启动一个控制台消费者

```sh
kafka-console-consumer.sh --bootstrap-server kafka01:9092 --topic TestComposeTopic --from-beginning
```

###   查看消费组

```sh
kafka-consumer-groups.sh --bootstrap-server 10.8.169.156:9092 --describe  --all-groups |grep CCS-Harbour-Vehicle-grantedArea  
```

### 删除消费组

```sh
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --delete --group my-group
```

### 查询分区消息数

```sh
kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list kafka01:9092 --topic topic
```

