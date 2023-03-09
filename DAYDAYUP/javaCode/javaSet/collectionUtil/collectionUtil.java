package javaSet.collectionUtil;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;

//java提供的集合工具类
public class collectionUtil {
    public static void main(String[] args) {
        var nums = new ArrayList();
        nums.add(1);
        nums.add(2);
        nums.add(6);
        nums.add(4);
        nums.add(0);
        Collections.reverse(nums);
        Collections.sort(nums);
        System.out.println(nums);
    }
}
