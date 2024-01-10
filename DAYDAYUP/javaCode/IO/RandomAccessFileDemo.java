package IO;

import java.io.FileDescriptor;
import java.io.RandomAccessFile;

/**
 * @author tianmingbo
 */
public class RandomAccessFileDemo {
    public static void main(String[] args) throws Exception {
        RandomAccessFile file = new RandomAccessFile("/Users/tianmingbo/PycharmProjects/GOOD-GOOD-STUDY/DAYDAYUP/javaCode/IO/das.txt", "rw");
        file.setLength(10000);
        file.seek(10); //设置当前文件指针
        file.write("dali".getBytes());
        file.seek(100);
        file.write("hallo 大力".getBytes());
        file.writeChars("fnfsnijianfkjnih");
        file.close();
    }

}
