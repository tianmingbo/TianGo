package generic.typeWildcard;

import java.util.ArrayList;
import java.util.Collection;

//设定类型通配符的下限

public class MyUtil_2 {
    public static <T> T copy(Collection<? super T> dest, Collection<T> src) {
        T last = null;
        for (var ele : src) {
            last = ele;
            dest.add(ele);
        }
        return last;
    }

    public static void main(String[] args) {
        var ln = new ArrayList<Number>();
        var li = new ArrayList<Integer>();
        li.add(9);
        li.add(10);
        Integer last = copy(ln, li);
        System.out.println(ln);
        System.out.println(last);
    }
}
