package IO.NIO.channel;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

/**
 * @author tianmingbo
 */
public class FileChannelDemo {
    public static void main(String[] args) {
        Path sourcePath = Paths.get("IO/NIO/channel/das.txt");
        Path destPath = Paths.get("IO/NIO/channel/das1.txt");
        try (FileChannel srcChannel = FileChannel.open(sourcePath,
                StandardOpenOption.READ);
             FileChannel destChannel = FileChannel.open(destPath,
                     StandardOpenOption.WRITE, StandardOpenOption.CREATE, StandardOpenOption.READ)) {
            //1.使用FileChannel 配合 ByteBuffer 缓冲区实现文件复制的功能
            ByteBuffer buffer = ByteBuffer.allocate(1024);

            while (srcChannel.read(buffer) != -1) {
                buffer.flip(); //获取buffer中的内容
                destChannel.write(buffer);
                buffer.clear(); //重置buffer,便于复用buffer
            }
            //2.使用内存映射文件（MappedByteBuffer）的方式实现文件复制的功能(直接操作缓冲区)
            long fileSize = srcChannel.size();
            MappedByteBuffer sourceMappedBuffer = srcChannel.map(FileChannel.MapMode.READ_ONLY, 0, fileSize);
            MappedByteBuffer destinationMappedBuffer = destChannel.map(FileChannel.MapMode.READ_WRITE, 0, fileSize);

            for (int i = 0; i < fileSize; i++) {
                byte b = sourceMappedBuffer.get(i);
                destinationMappedBuffer.put(i, b);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        //3.使用FileChannel的transferTo方法实现文件复制的功能
        try (FileChannel sourceChannel = FileChannel.open(sourcePath, StandardOpenOption.READ);
             FileChannel destinationChannel = FileChannel.open(destPath, StandardOpenOption.CREATE, StandardOpenOption.WRITE)) {

            long position = 0;
            long count = sourceChannel.size();

            // 循环传输，直到所有字节都被传输
            while (position < count) {
                long transferred = sourceChannel.transferTo(position, count - position, destinationChannel);
                position += transferred;
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
