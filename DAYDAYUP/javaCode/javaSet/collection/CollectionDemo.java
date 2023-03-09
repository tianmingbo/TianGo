package javaSet.collection;

import java.util.ArrayList;
import java.util.HashSet;

public class CollectionDemo {
    public static void main(String[] args) {
        var c = new ArrayList();
        c.add("tian");
        c.add(1);
        c.remove("1");
        c.add("mingbo");
        System.out.println(c);
        var book = new HashSet();
        book.add("java");
        book.add("android");
        System.out.println(book);
        c.addAll(book); //两个collection相加，java中可以list，set，queue相加
        System.out.println(c);
        c.clear();
        System.out.println(c);
    }
}
