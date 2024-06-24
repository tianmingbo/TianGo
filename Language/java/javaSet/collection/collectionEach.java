package javaSet.collection;

import java.util.HashSet;

public class collectionEach {
    public static void main(String[] args) {
        var books = new HashSet();
        books.add("java");
        books.add("python");
        books.add("js");
        books.add("android");
        books.forEach(obj-> System.out.println(obj));
    }
}
