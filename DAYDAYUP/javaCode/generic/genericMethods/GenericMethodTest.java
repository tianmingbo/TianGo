package generic.genericMethods;

import java.util.ArrayList;
import java.util.Collection;

//泛型方法
public class GenericMethodTest {
    static <T> void fromArrayToCollection(T[] a, Collection<T> c) {
        for (T o : a) {
            c.add(o);
        }
    }

    public static void main(String[] args) {
        var oa = new Object[100];
        Collection<Object> co = new ArrayList<>();
        //T代表Object类型
        fromArrayToCollection(oa, co);
//        System.out.println(co);
        var ia = new Integer[100];
        Collection<String> cs = new ArrayList<>();
//        fromArrayToCollection(ia, cs); 编译错误，因为ia是一个Integer数组，T代表的是String类型，Integer不是String的子类
    }

}
