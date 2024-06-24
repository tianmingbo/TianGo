package javaSet.Array;

import java.util.Arrays;

public class Demo {
    public static void main(String[] args) {
        int[] a = {1, 3, 4, 5, 6}; //静态初始化
        System.out.println(Arrays.toString(a));
        int[] prices = new int[5];
        var prices2 = new int[5];
        prices[3] = 10;
        System.out.println(Arrays.toString(prices));
        //foreach循环
        for (int num : prices) {
            System.out.println(num);
        }
    }
}
