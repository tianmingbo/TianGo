package javaSet.list;

import java.util.ArrayList;
import java.util.ListIterator;

public class ListIteratorDemo {
    public static void main(String[] args) {
        ArrayList<String> bookList = new ArrayList<>();
        bookList.add("js");
        bookList.add("python");
        bookList.add("java");
        System.out.println(bookList);
        ListIterator<String> list = bookList.listIterator(); //迭代器
        while (list.hasNext()) {
            list.next(); //
            list.add("-----------------"); //list 可以add
        }
        while (list.hasPrevious()) {
            System.out.println(list.previous()); //逆序输出
        }
    }
}
