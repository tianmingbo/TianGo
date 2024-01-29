package Nio.NioDiscard;

import util.Logger;
import org.junit.Test;

import java.nio.ByteBuffer;
import java.nio.channels.Pipe;

public class PipeDemo {
    @Test
    public void testPipe() throws Exception {
        String msg = "疯狂创客圈 高并发 研习社群!";
        Pipe pipe = Pipe.open();
        // 用于发送数据的SinkChannel
        Pipe.SinkChannel sinkChannel = pipe.sink();
        sinkChannel.write(ByteBuffer.wrap((msg).getBytes())); // 发送数据

        // 用于接收数据的SourceChannel
        Pipe.SourceChannel sourceChannel = pipe.source();
        ByteBuffer byteBuffer = ByteBuffer.allocate(msg.length());
        sourceChannel.read(byteBuffer);                       // 读取数据
        Logger.tcfo(new String(byteBuffer.array()));   // 打印数据
    }



}
