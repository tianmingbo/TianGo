### TCP超时与重传

### 基于计时器的重传

#### RTO计算公式

$$
EstimatedRTT = （1 - α） * EstimatedRTT + α * SampleRTT；  EstimatedRTT是SampleRTT的均值。α 一般是0.125
DevRTT = （1 - β） * DevRTT + β * | SampleRTT - EstimatedRTT |；DevRTT用于估算SampleRTT偏离EstimatedRTT的程度，β一般是0.25
Timeoutinterval(RTO) = EstinMrtedRTT + 4 * DevRTT； RTO要略大于RTT
$$

### 快速重传

当收到三个相同的 ACK 报文时，会在定时器过期之前，重传丢失的报文段。

```
事件：收到ACK,y是ACK的seq
  if （y > SendBase） {
  SendBase=y
  if （当前仍无任何应答报文段）
    启动定时器 ，
  }
  else {
  	/*对已经确认的报文段的一个冗余ACK */
    对y收到的冗余ACK数加1
    if （y==3 收到的冗余ACK数）
      /★ TCP快速重传*/
      重新发送具有序号y的报文段
  } 
  break；
  

```

### 带选择确认的重传  SACK

> **将已收到的数据的信息发送给「发送方」**，这样发送方就可以知道哪些数据收到了，哪些数据没收到，知道了这些信息，就可以**只重传丢失的数据**。**避免快速重传的回退N问题**

