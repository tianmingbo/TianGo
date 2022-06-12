package Object.processObject;

//
class Person {
    public int a = 5;

    public String toString() {
        System.out.println(Person.class);
        return "call toString()";
    }
}

public class PrintObject {
    public static void main(String[] args) {
        var people = new Person();
        System.out.println(people); //直接输出实例，会默认调用类中的toString()方法，类似Python的__str__
    }
}
