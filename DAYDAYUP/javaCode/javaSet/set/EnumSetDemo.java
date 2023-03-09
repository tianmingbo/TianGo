package javaSet.set;

import java.util.EnumSet;

enum Season {
    SPRING, SUMMER, FALL, WINTER
}

/**
 * EnumSet是所有set中性能最好的，但是只能添加枚举类中的元素。
 * set的实现类HashSet，TreeSet，EnumSet都是线程不安全的。
 * */
//专门为枚举类设计的set，只能添加枚举类中存在的元素
public class EnumSetDemo {
    public static void main(String[] args) {
        var es1 = EnumSet.allOf(Season.class);
        System.out.println(es1);
        es1.add(Season.valueOf("test")); //不能添加别的元素
    }
}
