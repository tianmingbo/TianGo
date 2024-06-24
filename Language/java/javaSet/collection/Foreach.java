package javaSet.collection;

import java.util.HashSet;

//使用foreach遍历集合
public class Foreach {
    public static void main(String[] args) {
        var books = new HashSet();
        books.add("java");
        books.add("python");
        books.add("js");
        books.add("android");
        for (var obj : books) {
            var book = (String) obj;
            System.out.println(book);
            //foreach遍历也不能删除集合中的元素
        }
    }
}
