package IO.NIO.channel;

import java.io.File;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.nio.channels.FileChannel;

public class FileNIOCopyDemo {
    public static void nioCopyFile() {

        File srcFile = new File("IO/NIO/channel/das.txt");
        File destFile = new File("IO/NIO/channel/das1.txt");

        try {
            //如果目标文件不存在，则新建
            if (!destFile.exists()) {
                destFile.createNewFile();
            }

            long startTime = System.currentTimeMillis();

            FileChannel inChannel = new FileInputStream(srcFile).getChannel();
            FileChannel outchannel = new FileOutputStream(destFile).getChannel();

            int length = -1;
            ByteBuffer buf = ByteBuffer.allocateDirect(2);
            //从输入通道读取到buf
            while ((length = inChannel.read(buf)) != -1) {
                System.out.println("读取字节数:" + length);
                //翻转buf,变成成读模式
                buf.flip();

                int outlength = 0;
                //将buf写入到输出的通道
                while ((outlength = outchannel.write(buf)) != 0) {
                    System.out.println("写入字节数：" + outlength);
                }
                //清除buf,变成写入模式
                buf.clear();
            }


            //强制刷新磁盘
            outchannel.force(true);
            long endTime = System.currentTimeMillis();
            System.out.println(" 复制毫秒数：" + (endTime - startTime));

        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    public static void main(String[] args) {
        nioCopyFile();
    }
}
