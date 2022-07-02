package javaSet.collectionUtil;

import java.util.List;
import java.util.Map;
import java.util.Set;

//创建不可变集合
public class unWrite {
    public static void main(String[] args) {
        var set = Set.of("java", "py");
        var list = List.of(1, 2, 3, 0);
        var map = Map.of("name", "tian");
        var map2 = Map.ofEntries(Map.entry("name", "tian"));//功能同上
    }
}
