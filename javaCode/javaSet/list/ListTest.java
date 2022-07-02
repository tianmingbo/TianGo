package javaSet.list;

import java.util.ArrayList;

//list
public class ListTest {
    public static void main(String[] args) {
        var books = new ArrayList();
        books.add("java");
        books.add("python");
        books.add("js");
        books.add("android");
        books.add(1, "c");
        books.set(1, "C++");
        books.remove(0);
        System.out.println(books);
        for (var i = 0; i < books.size(); i++) {
            System.out.println(books.get(i));
        }
        books.sort((o1, o2) -> ((String) o1).length() - ((String) o2).length()); //排序
        System.out.println(books);
        books.replaceAll(ele -> ((String) ele).toUpperCase());
        System.out.println(books); //[JS, C++, PYTHON, ANDROID]
    }
}
