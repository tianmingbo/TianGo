package javaSet.collection;

import java.util.HashSet;

public class Iterator {
    public static void main(String[] args) {
        var books = new HashSet<String>();
        books.add("java");
        books.add("python");
        books.add("js");
        books.add("android");
        var item = books.iterator();//获取迭代器
        while (item.hasNext()) {
            String book = item.next();
            if (book.equals("java")) {
                item.remove(); //使用iterator遍历集合时，集合里的元素不能被改变
            }
            System.out.println(book);
        }
        System.out.println(books);
    }
}
