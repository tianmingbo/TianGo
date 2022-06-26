package BaseMoudle.StringClass;
/*
 * String不可改变、
 * StringBuffer和StringBuilder可变。
 * StringBuffer线程安全
 * */

import java.util.Arrays;

public class UseString {
    public static void main(String[] args) {
        var s = "fuck you";
        var s2="test";
        var s3=new String("test");
        System.out.println(s.charAt(5));//取出第五位
        System.out.println(s.compareTo(s2));
        System.out.println(s3.getBytes());
    }
}
