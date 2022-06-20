package BaseMoudle.interaction;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

//捕获键盘输入
public class ScannerKeyBoard {
    public static void main(String[] args) throws FileNotFoundException {
//        var sc = new Scanner(System.in);
//        //使用\n换行
//        sc.useDelimiter("\n");
//        while (sc.hasNext()) {
//            System.out.println(sc.next());
//        }
        var file = new Scanner(new File("/Users/tianmingbo/PycharmProjects/GOOD-GOOD-STUDY/javaCode/BaseMoudle/interaction/ScannerKeyBoard.java"));
        while (file.hasNextLine()) {
            System.out.println(file.nextLine());
        }
    }
}
