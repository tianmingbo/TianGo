package Object.processObject;

class Person2 {
    private String name;
    private String id;

    public Person2(String name, String id) {
        this.setName(name);
        this.setId(id);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    //重写，可以自己添加怎么样还相等
    public boolean equals(Object obj) {
        if (this == obj) {
            //如果两个对象为同一对象
            return true;
        }
        //只有当obj是Person2的对象
        if (obj != null && obj.getClass() == Person2.class) {
            var personObj = (Person2) obj;
            //判断id是否相同
            return this.getId().equals(personObj.getId());
        }
        return false;
    }
}

public class OverrideEquals {
    public static void main(String[] args) {
        var p1 = new Person2("tian", "123456");
        var p2 = new Person2("dali", "123456");
        System.out.println(p1.equals(p2)); //true 因为id相等
    }
}
