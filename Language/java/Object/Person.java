package Object;

public class Person {
    public String name;
    public int age;

    public static void say(String content) {
        System.out.println(content);
    }

    public static void main(String[] args) {
//        say("tewt");
        var p = new Person();
        p.name = "tian";
        say("test");
        System.out.println(p.name);
    }
}
