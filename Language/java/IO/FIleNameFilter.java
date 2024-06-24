package IO;

import java.io.File;

public class FIleNameFilter {
    public static void main(String[] args) {
        var file = new File("C:\\tmb\\GOOD-GOOD-STUDY\\javaCode");
        String[] nameList = file.list((dir, name) -> name.length() > 5);
        for(var i :nameList){
            System.out.println(i);
        }
    }
}
