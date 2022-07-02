package javaSet.collectionUtil;

import java.util.*;

//集合线程安全工具
public class syncControl {
    public static void main(String[] args) {
        var list= Collections.synchronizedList(new ArrayList());
        var hashset= Collections.synchronizedSet(new HashSet());
        var map= Collections.synchronizedMap(new HashMap());
    }
}
