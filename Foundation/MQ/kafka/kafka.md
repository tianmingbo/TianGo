### 如何实现高吞吐量、低延时

- 大量使用操作系统页缓存， 内存操作速度快且命中率高。
- Kafka 不直接参与物理 I/O 操作，而是交给操作系统来完成。
- 采用追加写入。
- 使用以 sendfile 为代表的零拷贝技术加强网络间的数据传输效率。

### 分区策略

- 顺序分配
- 随机分配
- 按消息键保存
- 自定义分配

### 怎么保证消息不丢失

1. 不要使用 producer.send(msg)，而要使用 producer.send(msg, callback)。记住，一定要使用带有回调通知的 send 方法。
2. 设置 acks = all。acks 是 Producer 的一个参数，代表了你对“已提交”消息的定义。如果设置成 all，则表明所有副本 Broker 都要接收到消息，该消息才算是“已提交”。这是最高等级的“已提交”定义。
3. 设置 retries 为一个较大的值。这里的 retries 同样是 Producer 的参数。当出现网络的瞬时抖动时，消息发送可能会失败，此时配置了etries > 0 的 Producer 能够自动重试消息发送，避免消息丢失。
4. 设置 unclean.leader.election.enable = false。这是 Broker 端的参数，它控制的是哪些 Broker 有资格竞选分区的 Leader。如果一个 Broker 落后原先的 Leader 太多，那么它一旦成为新的 Leader，必然会造成消息的丢失。故一般都要将该参数设置成 false，即不允许这种情况的发生。
5. 设置 replication.factor >= 3。这也是 Broker 端的参数。其实这里想表述的是，最好将消息多保存几份，毕竟目前防止消息丢失的主要机制就是冗余。
6. 设置 min.insync.replicas > 1。这依然是 Broker 端参数，控制的是消息至少要被写入到多少个副本才算是“已提交”。设置成大于 1 可以提升消息持久性。在实际环境中千万不要使用默认值 1。
7. 确保 replication.factor > min.insync.replicas。如果两者相等，那么只要有一个副本挂机，整个分区就无法正常工作了。我们不仅要改善消息的持久性，防止数据丢失，还要在不降低可用性的基础上完成。推荐设置成 replication.factor = min.insync.replicas +1。
8. 确保消息消费完成再提交。Consumer 端有个参数 enable.auto.commit，最好把它设置成 false，并采用手动提交位移的方式。就像前面说的，这对于单 Consumer 多线程处理的场景而言是至关重要的。

### 消息可靠性保证

- 最多一次
- 至少一次
- 精确一次：通过幂等性和事务实现

### 消费者组

1. Consumer Group下可以由一个或多个Consumer实例；
2. Group Id是一个字符串，在一个kafka集群中，它标识唯一的一个Consumer Group
3. 一个Topic的一个分区，只能给一个Consumer Group中的一个Consumer消费。

### 位移主题（__consumer_offsets）

> 存 Kafka 消费者的位移信息。 Key: <GroupID，主题名，分区号 >