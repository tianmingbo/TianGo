package Object.polymorphism;

/**
 * instanceof 前面和后面的要么有父子继承关系，
 * 要么是同一个类型
 */
public class InstanceofTest {
    public static void main(String[] args) {
        var hello = "hello";
//        System.out.println(hello instanceof Math);//String和Math不存在继承关系，所以报错
        System.out.println(hello instanceof String);
    }
}
