package javaSet.collection;

import java.util.HashSet;

public class PredicateTest {
    public static void main(String[] args) {
        var books = new HashSet();
        books.add("java");
        books.add("python");
        books.add("js");
        books.add("android");
        //removeI方法的类型是Predicate
        books.removeIf(ele -> ((String) ele).length() < 10);
        System.out.println(books);
    }
}
