package IO.FileStream;

import java.io.*;
import java.util.Arrays;

/**
 * @author tianmingbo
 */
public class FileInput {
    public static void main(String[] args) throws IOException {
        String path = "./IO/FileStream/io.md";
        String dirPath = "./IO/FileStream/test/test1";
        File file = new File(path);
        File dir = new File(dirPath);
        System.out.println(file.getAbsoluteFile()); //绝对路径
        System.out.println(file.getPath()); //构造路径
        System.out.println(file.length()); //文件长度
        System.out.println(file.getName()); //获取文件名
        System.out.println(file.canWrite());
        System.out.println(file.exists()); //文件或目录是否存在
        System.out.println(file.isDirectory()); //是否目录
//        System.out.println(dir.mkdir());//创建目录
        System.out.println(dir.mkdirs());//创建多层目录
        String[] files = dir.list();
        for (String s : files) {
            System.out.println(s);
        }
    }
}
