package Object.Final;

//final修饰的方法不可被重写
class PrivateFinalMethod {
    private final void test() {
    }
}

class FinalMethod extends PrivateFinalMethod {
    //父类中的test是私有方法，子类中不可见。以下是重新定义了一个新方法而已
    public final void test() {
    }

    //final修饰的方法不可以重写，但是可以重载
    public final void test(String id) {

    }
}
