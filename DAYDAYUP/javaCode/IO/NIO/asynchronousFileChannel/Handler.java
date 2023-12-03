package IO.NIO.asynchronousFileChannel;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.AsynchronousFileChannel;
import java.nio.channels.CompletionHandler;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicLong;

/**
 * @author tianmingbo
 */
public class Handler {
    public static void main(String[] args) throws Exception {
        // 创建文件路径
        Path path = Paths.get("IO/NIO/channel/das1.txt");
        // 打开文件通道
        AsynchronousFileChannel fileChannel = AsynchronousFileChannel.open(path, StandardOpenOption.READ);
        // 创建缓冲区
        ByteBuffer buffer = ByteBuffer.allocate(1024);
        // 创建文件指针并初始化为0
        AtomicLong position = new AtomicLong(0);
        // 用于在异步操作完成时通知主线程
        CountDownLatch latch = new CountDownLatch(1);

        // 使用异步读取函数进行文件读取
        fileChannel.read(buffer, position.get(), null, new CompletionHandler<Integer, Object>() {
            @Override
            public void completed(Integer bytesRead, Object attachment) {
                // 成功回调
                if (bytesRead > 0) {
                    // 更新文件指针
                    position.addAndGet(bytesRead);
                    // 处理读取到的数据
                    buffer.flip();
                    byte[] data = new byte[buffer.limit()];
                    buffer.get(data);
                    System.out.print(new String(data));
                    buffer.clear();

                    // 继续读取文件
                    fileChannel.read(buffer, position.get(), attachment, this);
                } else {
                    latch.countDown();
                    try {
                        fileChannel.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            public void failed(Throwable exc, Object attachment) {
                // 处理异常
                System.out.println("Error: " + exc.getMessage());
                latch.countDown();
            }
        });

        // 等待读取完成
        latch.await();
    }

}
