package Object.packaging;

public class AutoBoxingUnboxing {
    public static void main(String[] args) {
        //自动装箱，就是可以直接把基本类型变量赋值给包装类
        Integer inObj = 5;
        System.out.println(inObj);
        //自动拆箱，可以把包装类对象直接赋值给一个对应的基本类型变量
        int it = inObj;
    }
}
