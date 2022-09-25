package IO;

import java.io.*;

class charStream {
    public static void test() {
        //FileWriter可以直接输出字符串
        try (var newFile = new FileWriter("test.txt");) {
            newFile.write("大力超级牛！");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


}

class byteStream {
    public static void test() {
        try {
            var fis = new FileInputStream("C:\\tmb\\GOOD-GOOD-STUDY\\javaCode\\IO\\FileInputStreamTest.java");
            var outFile = new FileOutputStream("test.txt");
            var bbuf = new byte[1024];
            var hasRead = 0;
            while ((hasRead = fis.read(bbuf)) > 0) {
                outFile.write(bbuf, 0, hasRead);
            }
        } catch (IOException ios) {
            ios.printStackTrace();
        }
    }
}

public class outputStreamTest {
    public static void main(String[] args) {
//        byteStream.test();
        charStream.test();
    }
}
