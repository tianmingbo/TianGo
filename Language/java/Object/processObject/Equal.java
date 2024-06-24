package Object.processObject;

public class Equal {
    public static void main(String[] args) {
        //只要是常量且是数值类型，只要值相等，就返回true，
        //对于引用，只有引用执行的地址相同，才返回true
        var it = 65;
        var fl = 65.0f;
        var ch = 'A';
        System.out.println(it == fl);
        System.out.println(it == ch);
        var str = new String("hello");
        var str2 = new String("hello");
        System.out.println(str == str2);
        //equals也是根据是否执行同一地址来判断的，和'=='一样
        //String重写了equals方法，只要字符串相同，就返回true
        System.out.println(str.equals(str2));
    }
}
