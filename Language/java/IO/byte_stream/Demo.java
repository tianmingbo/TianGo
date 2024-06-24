package IO.byte_stream;

import java.io.*;


/**
 * 字节流
 * <p>out:</p>
 * 1、 close() ：关闭此输出流并释放与此流相关联的系统资源。
 * 2、 flush() ：刷新此输出流并强制缓冲区的字节被写入到目的地。
 * 3、 write(byte[] b)：将 b.length 个字节从指定的字节数组写入此输出流。
 * 4、 write(byte[] b, int off, int len) ：从指定的字节数组写入 len 字节到此输出流，从偏移量 off开始。 也就是说从off个字节数开始一直到len个字节结束
 * <p>in</p>
 * 1、close() ：关闭此输入流并释放与此流相关的系统资源。
 * 2、int read()： 从输入流读取数据的下一个字节。
 * 3、read(byte[] b)： 该方法返回的 int 值代表的是读取了多少个字节，读到几个返回几个，读取不到返回-1
 *
 * @author tianmingbo
 */

public class Demo {
    public static void main(String[] args) throws IOException {
        FileInputStream fis = new FileInputStream("./IO/byte_stream/tmp.png");
        FileOutputStream fos = new FileOutputStream("./IO/byte_stream/tmp2.png");
        byte[] buf = new byte[1024];
        int count;
        while ((count = fis.read(buf)) != -1) {
            // 读取原始图片文件并将数据写入复制后的图片文件
            fos.write(buf, 0, count);
            System.out.println(new String(buf));
        }
        fis.close();
        fos.close();
    }
}
