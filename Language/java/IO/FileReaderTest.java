package IO;

import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;

public class FileReaderTest {
    public static void main(String[] args) throws IOException {
        //字符输入流，java中char占2个字节，16位
        var fis = new FileReader("C:\\tmb\\GOOD-GOOD-STUDY\\javaCode\\IO\\FileInputStreamTest.java");
        var bbuf = new char[2];
        var hasRead = 0;
        //循环读取
        while ((hasRead = fis.read(bbuf)) > 0) {
            System.out.println(hasRead);
            System.out.println(new String(bbuf, 0, hasRead));
        }
    }
}
