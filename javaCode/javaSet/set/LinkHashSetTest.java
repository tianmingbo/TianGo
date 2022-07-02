package javaSet.set;

import java.util.LinkedHashSet;

//有序的set，按插入顺序排序
public class LinkHashSetTest {
    public static void main(String[] args) {
        var books = new LinkedHashSet();
        books.add("python");
        books.add("python1");
        books.add("python2");
        books.add("python3");
        books.forEach(ele -> System.out.println(ele)); //输出是有序的
    }
}
