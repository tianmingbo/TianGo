package IO;

import java.io.FileInputStream;
import java.io.IOException;

public class FileInputStreamTest {
    public static void main(String[] args) throws IOException {
        //字节输入流
        var fis = new FileInputStream("C:\\tmb\\GOOD-GOOD-STUDY\\javaCode\\IO\\FileInputStreamTest.java");
        var bbuf = new byte[1024];
        var hasRead = 0;
        //循环读取
        while ((hasRead = fis.read(bbuf)) > 0) {
            System.out.println(new String(bbuf, 0, hasRead));
        }
    }
}
