package IO;


import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;

public class PrintStreamTest {
    public static void main(String[] args) {
        try (var fos = new FileOutputStream("test.txt");
             var ps = new PrintStream(fos);) {
            ps.println("test");
            ps.println(new PrintStreamTest());

        } catch (IOException io) {
            io.printStackTrace();
        }
    }
}
