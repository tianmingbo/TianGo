package javaSet.list;

import java.util.ArrayList;
import java.util.Iterator;

//list
public class ListTest {
    public static void main(String[] args) {
        ArrayList<String> list = new ArrayList<>();
        list.add("py");
        list.add("java");
        list.add("C");
        for (String s : list) {
            System.out.println(s);
        }
        Iterator<String> iterator = list.iterator();
        System.out.println("*****************");
        while (iterator.hasNext()) {
            String next = iterator.next();
            if("py".equals(next)){
                iterator.remove();
            }
            System.out.println(next);
        }
        System.out.println("*****************");
        for (int i = 0; i < list.size(); i++) {
            System.out.println(list.get(i));
        }
    }
}
