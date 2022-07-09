package generic;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

//菱形语法
public class Diamind_1 {
    public static void main(String[] args) {
        List<String> books = new ArrayList<>();
        books.add("python");
        books.add("java");
        System.out.println(books);
        Map<String, List<String>> schoolsInfo = new HashMap<>();
        List<String> schools = new ArrayList<>();
        schools.add("sanxingdong");
        schools.add("demo");
        schoolsInfo.put("sun", schools);
        schoolsInfo.forEach((k, v) -> System.out.println(k + ':' + v));
    }
}
