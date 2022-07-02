package javaSet.set;

import java.util.TreeSet;

//元素排序状态，采用红黑树来存储元素，treeset中添加的应该是同一类的对象
public class TreeSetTest {
    public static void main(String[] args) {
        var nums = new TreeSet();
        nums.add(1);
        nums.add(-1);
        nums.add(10);
        nums.add(8);
        System.out.println(nums);
        System.out.println(nums.first());
        System.out.println(nums.last());
        System.out.println(nums.headSet(4)); //返回小于4的子集，不包含4
        System.out.println(nums.tailSet(4)); //返回大于4的元素，包括4
    }
}
