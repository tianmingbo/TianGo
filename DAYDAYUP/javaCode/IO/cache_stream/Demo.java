package IO.cache_stream;

import java.io.*;
import java.util.HashMap;

/**
 * @author tianmingbo
 */
public class Demo {
    public static void exec(String path) throws IOException {
        HashMap<Integer, String> data = new HashMap<>();
        try (BufferedReader br = new BufferedReader(new FileReader(path));
             BufferedWriter bw = new BufferedWriter(new FileWriter("./IO/cache_stream/tmp.txt"))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (line.length() > 0) {
                    String[] split = line.split("\\.");
                    data.put(Integer.valueOf(split[0]), split[1]);
                }

            }
            for (int i = 1; i < data.size(); i++) {
                String s = data.get(i);
                bw.write(i + "." + s);
                bw.newLine();
            }
        }
    }

    public static void main(String[] args) throws IOException {
        long start = System.currentTimeMillis();
        //字节缓冲流
        try (BufferedInputStream bis = new BufferedInputStream(new FileInputStream("./IO/cache_stream/tmp.mp4"));
             BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream("./IO/cache_stream/tmp2.mp4"));) {
            int b;
            byte[] buf = new byte[8 * 1024];
            while ((b = bis.read(buf)) != -1) {
                bos.write(buf, 0, b);
            }
        }
        long end = System.currentTimeMillis();
        System.out.println(end - start);
        //字节缓冲流
        try (BufferedReader br = new BufferedReader(new FileReader("./IO/cache_stream/tmp.mp4"));
             BufferedWriter bw = new BufferedWriter(new FileWriter("./IO/cache_stream/tmp3.mp4"))) {
            int c;
            while ((c = br.read()) != -1) {
                bw.write(c);
            }
        }
        Demo.exec("./IO/cache_stream/tt.log");
    }
}
