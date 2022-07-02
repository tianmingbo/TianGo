package javaSet.collection;

import java.util.HashSet;
import java.util.stream.IntStream;

//
public class Stream {
    static void collectionStream() {
        var books = new HashSet();
        books.add("java");
        books.add("python");
        books.add("js");
        books.add("android");
        //stream中间方法不会终止,如filter、mapToxxx、sorted
        books.stream().mapToInt(ele -> ((String) ele).length()).forEach(System.out::println);
        //count、min、max、anyMatch等是末端方法，使用后会终止流
        System.out.println(books.stream().filter(ele -> ((String) ele).contains("java")).count());
    }

    static void intStream() {
        var is = IntStream.builder().add(12).add(13).add(1).build();
//        System.out.println(is.allMatch(ele -> ele * ele > 20));
//        System.out.println(is.anyMatch(ele -> ele * ele > 20));
        System.out.println(is.max().getAsInt());
    }

    public static void main(String[] args) {
        Stream.collectionStream();
        Stream.intStream();
    }
}
