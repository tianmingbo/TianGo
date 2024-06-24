package Object.Final;

//final修饰引用类型时，只保证引用的地址不变，不保证地址中存储的数据不变
class Person {
    private int age;

    public Person() {
    }

    public Person(int age) {
        this.age = age;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}

public class FinalReference {
    public static void main(String[] args) {
        final var p = new Person(18);
        p.setAge(34);
//        p=null; p不能指向别的地址
        System.out.println(p.getAge());
    }
}
