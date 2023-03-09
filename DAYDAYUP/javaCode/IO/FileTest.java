package IO;

import java.io.File;
import java.io.IOException;

public class FileTest {
    public static void main(String[] args) throws IOException {
        File file = new File("test.txt"); //创建一个文件对象，只能获取路径、名字……，不能读写文件内容
        System.out.println(file.getAbsoluteFile());
        System.out.println(file.getName());
        System.out.println(file.getParent());
        System.out.println(file.createNewFile());
        System.out.println(file.mkdir());
        File[] roots=File.listRoots();
        for(var root : roots){
            System.out.println(root);
        }
    }
}
