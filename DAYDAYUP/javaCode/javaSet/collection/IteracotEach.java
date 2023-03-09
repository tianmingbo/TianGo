package javaSet.collection;

import java.util.HashSet;

//使用lambda遍历Iterator
public class IteracotEach {
    public static void main(String[] args) {
        var books = new HashSet();
        books.add("java");
        books.add("python");
        books.add("js");
        books.add("android");
        var it=books.iterator();
        it.forEachRemaining(obj-> System.out.println(obj));
    }
}
