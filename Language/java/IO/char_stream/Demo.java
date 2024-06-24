package IO.char_stream;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

/**
 * <p>in</p>
 * FileReader:
 * 1、close()：关闭此流并释放与此流相关的系统资源。
 * 2、read()：从输入流读取一个字符。
 * 3、read(char[] cbuf)：从输入流中读取一些字符，并将它们存储到字符数组 cbuf中
 * <p>out</p>
 * FileWriter:
 * 1、write(int c) 写入单个字符。
 * 2、write(char[] cbuf) 写入字符数组。
 * 3、write(char[] cbuf, int off, int len) 写入字符数组的一部分，off为开始索引，len为字符个数。
 * 4、write(String str) 写入字符串。
 * 5、write(String str, int off, int len) 写入字符串的某一部分，off 指定要写入的子串在 str 中的起始位置，len 指定要写入的子串的长度。
 * 6、flush() 刷新该流的缓冲。
 * 7、close() 关闭此流，但要先刷新它。
 *
 * @author tianmingbo
 */
public class Demo {
    public static void main(String[] args) throws IOException {
        FileReader fr = new FileReader("./IO/char_stream/a.txt");
        FileWriter fw = new FileWriter("./IO/char_stream/a1.txt");
        int b;
        char[] buf = new char[1024];
        while ((b = fr.read(buf)) != -1) {
            fw.write(buf, 0, b);
            System.out.println(new String(buf, 0, b));
        }
        fw.flush(); //刷新缓冲区，流对象可以继续使用。
        fw.close(); //先刷新缓冲区，然后通知系统释放资源。流对象不可以再被使用了。
        fr.close();
    }
}
