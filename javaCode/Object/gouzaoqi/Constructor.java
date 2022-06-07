package Object.gouzaoqi;

//构造器重载
public class Constructor {
    public String name;
    public int age;

    public Constructor() {
    }

    public Constructor(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public static void main(String[] args) {
        var obj = new Constructor("tian", 18);
        System.out.println(obj.name + obj.age);
    }
}
