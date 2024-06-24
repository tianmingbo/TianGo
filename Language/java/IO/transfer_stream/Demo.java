package IO.transfer_stream;

import java.io.*;
import java.nio.charset.StandardCharsets;

public class Demo {
    public static void main(String[] args) throws IOException {
        /*
          OutputStreamWriter: 字符输出流转字节输出流
          InputStreamReader: 将字节流转换为字符流
          */
        String path = "./IO/transfer_stream/tmp.txt";
        try (OutputStreamWriter osw = new OutputStreamWriter(new FileOutputStream("./IO/transfer_stream/tmp2.txt"), "GBK");
             InputStreamReader isr = new InputStreamReader(new FileInputStream("./IO/transfer_stream/tmp.txt"), StandardCharsets.UTF_8)
        ) {
            int len;
            char[] buf = new char[10];
            while ((len = isr.read(buf)) != -1) {
                osw.write(buf, 0, len);
                System.out.println(new String(buf, 0, len));
            }
        }

    }
}
