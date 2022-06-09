package Object.packaging;

public class Primitive2String {
    public static void main(String[] args) {
        var intStr = "123";
        var it1 = Integer.valueOf(intStr);//字符串转基本数据类型，使用valueOf()或parseXXX()
        var it2 = Integer.parseInt(intStr);
        System.out.println(it1);
        System.out.println(it2);
        var ftStr = String.valueOf(2.3f); //转字符串
    }
}
