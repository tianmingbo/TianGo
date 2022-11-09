package com.xiaojianbang.ndk;

public class NDKDemo {
    public static String privateStaticStringField = "this is privateStaticStringField";
    public static String publicStaticStringField = "this is publicStaticStringField";
    public byte[] byteArray = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    public String privateStringField = "this is privateStringField";
    public String publicStringField = "this is publicStringField";

    public NDKDemo() {
        Log.d("xiaojianbang", "this is ReflectDemo()");
    }

    public NDKDemo(String str) {
        Log.d("xiaojianbang", "this is ReflectDemo(String str)");
    }

    public NDKDemo(String str, int i) {
        Log.d("xiaojianbang", i + " " + str);
        Log.d("xiaojianbang", "this is ReflectDemo(String str, int i)");
    }

    public static void publicStaticFunc() {
        Log.d("xiaojianbang", "this is publicStaticFunc");
    }

    public void publicFunc() {
        Log.d("xiaojianbang", "this is publicFunc");
    }

    public static int[] privateStaticFunc(String[] str) {
        StringBuilder retval = new StringBuilder();
        for (String i : str) {
            retval.append(i);
        }
        Log.d("xiaojianbang", "this is privateStaticFunc: " + retval.toString());
        return new int[]{100, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    }

    public String privateFunc(String str, int i) {
        Log.d("xiaojianbang", i + " this is privateFunc: " + str);
        return "this is from java";
    }

}

class Log {
    public static void d(String a, String b) {
        System.out.println(a + "\t" + b);
    }
}