package IO.NIO.asynchronousFileChannel;

import java.nio.ByteBuffer;
import java.nio.channels.AsynchronousFileChannel;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.concurrent.Future;

/**
 * @author tianmingbo
 */
public class future {
    public static void main(String[] args) throws Exception {
        Path path = Paths.get("IO/NIO/channel/das1.txt");
        //异步读取操作
        try (AsynchronousFileChannel fileChannel = AsynchronousFileChannel.open(path, StandardOpenOption.READ)) {
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            long position = 0;

            while (true) {
                //表示读取操作的结果
                Future<Integer> result = fileChannel.read(buffer, position);
                //检查异步操作是否完成
                while (!result.isDone()) {
                    // 在这里可以执行其他任务，例如处理其他 I/O 操作
                    System.out.println("正在读取数据...");
                }

                int bytesRead = result.get();
                if (bytesRead <= 0) {
                    break;
                }

                position += bytesRead;
                buffer.flip();

                byte[] data = new byte[buffer.limit()];
                buffer.get(data);
                System.out.println(new String(data));

                buffer.clear();
            }
        }

    }


}
