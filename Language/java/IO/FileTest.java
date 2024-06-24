package IO;

import java.io.*;

/**
 * @author tianmingbo
 */
public class FileTest {
    public static void main(String[] args) throws IOException {
//        BufferedInputStream inputStream = new BufferedInputStream(new FileInputStream("./IO/das.txt"));
//        byte[] bytes = new byte[1024];
//        int byteReader;
//        while ((byteReader = inputStream.read(bytes)) != -1) {
//            System.out.println(new String(bytes, 0, byteReader));
//        }
//        inputStream.close();
        BufferedOutputStream stream = new BufferedOutputStream(new FileOutputStream("./IO/das.txt"));
        byte[] buf;
        buf = "我是好人".getBytes();
        stream.write(buf);
        stream.flush();
        stream.close();
//        DataOutputStream das = new DataOutputStream(new FileOutputStream("./IO/das.txt"));
//        das.write("www".getBytes());
//        das.writeInt(100);
//        das.close();
    }
}
