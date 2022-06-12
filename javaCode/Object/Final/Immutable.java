package Object.Final;

//不可变类，当创建实例后，实例的实例变量不可修改
//8个包装类和java.lang.String都是不可变类
public class Immutable {
    //使用private和final修饰成员变量
    private final String detail;
    private final String postCode;

    //提供带参数的构造器，来初始化成员变量
    public Immutable(String detail, String postCode) {
        this.detail = detail;
        this.postCode = postCode;
    }

    //仅提供getter方法
    public String getDetail() {
        return detail;
    }

    public String getPostCode() {
        return postCode;
    }

    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj != null && obj.getClass() == Immutable.class) {
            var o = (Immutable) obj;
            return this.getDetail().equals(o.getDetail()) && this.getPostCode().equals(o.getPostCode());
        }
        return false;
    }

    public int hashCode() {
        return detail.hashCode() + postCode.hashCode() * 31;
    }

    public static void main(String[] args) {
        var test = new Immutable("1", "2");
//        test.postCode="dd";不可修改
    }
}

class CacheImmutable {
    private static int MAX_SIZE = 10;
    private static CacheImmutable[] cache = new CacheImmutable[MAX_SIZE];
    private static int pos = 0;
    private final String name;

    private CacheImmutable(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public static CacheImmutable valueOf(String name) {
        for (var i = 0; i < MAX_SIZE; i++) {
            if (cache[i] != null && cache[i].getName().equals(name)) {
                return cache[i];
            }
        }
        if (pos == MAX_SIZE) {
            //缓存已满，则覆盖
            cache[0] = new CacheImmutable(name);
            pos = 1;
        } else {
            //新建对象
            cache[pos++] = new CacheImmutable(name);
        }
        return cache[pos - 1];
    }

    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj != null && obj.getClass() == CacheImmutable.class) {
            var o = (CacheImmutable) obj;
            return name.equals(o.getName());
        }
        return false;
    }

    public int hashCode() {
        return name.hashCode();
    }
}