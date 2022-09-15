package javaSet.map;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.*;
import java.util.Map.Entry;

public class mapDemo {
    //字典实现
    static void hashMap() {
        var map = new HashMap();
        map.put("age", "18");
        map.put("name", "tian");
        map.put("hobby", "game");
//        System.out.println(map);
//        System.out.println(map.put("name", "dali")); //更新name的value，会返回原来的value
//        System.out.println(map.containsKey("age"));
//        System.out.println(map.keySet());//所有key
//        System.out.println(map.values()); //所有value
        for (var key : map.keySet()) {
            System.out.println(key);
            System.out.println(map.get(key));
        }
        Set<Entry<String, String>> entryseSet = map.entrySet();  //遍历

        for (Entry entry : entryseSet) {

            System.out.println(entry.getKey() + "," + entry.getValue());

        }
        map.forEach((k, v) -> System.out.println((String) k + (String) v));
    }

    //读写文件属性
    static void properties() throws Exception {
        var props = new Properties();
        props.setProperty("name", "tian");
        props.store(new FileOutputStream("a.ini"), "comment");
        var props1 = new Properties();
        props1.setProperty("age", "18");
        props1.load(new FileInputStream("a.ini"));
        System.out.println(props1);
    }

    //TreeMap继承sortedMap，红黑树数据结构
    static void treeMap() {
        var map = new TreeMap();
        map.put(4, "name");
        map.put(2, "age");
        map.put(3, "other");
        System.out.println(map);
        System.out.println(map.higherEntry(2));
    }

    public static void main(String[] args) throws Exception {
        mapDemo.hashMap();
//        mapDemo.properties();
//        mapDemo.treeMap();
    }
}
