package thread.Tools_15;

//为每一个使用该变量的线程都提供一个变量值的副本，使每一个线程可以独立地改变自己的副本，不会和其他线程的副本冲突
class Account {
    private ThreadLocal<String> name = new ThreadLocal<>();

    public Account(String str) {
        this.name.set(str);
        System.out.println("---" + this.name.get());
    }

    public String getName() {
        return this.name.get();
    }

    public void setName(String str) {
        this.name.set(str);
    }
}

class MyTest extends Thread {
    private Account account;

    public MyTest(Account account, String name) {
        super(name);
        this.account = account;
    }

    @Override
    public void run() {
        for (var i = 0; i < 10; i++) {
            //当i==6后，发现两个线程访问同一个账户出现的账户名不同
            if (i == 6) {
                account.setName(getName());
            }
            System.out.println(account.getName() + " account i value: " + i);
        }
    }
}

public class ThreadLocalTest {
    public static void main(String[] args) {
        var at = new Account("init name");
        /*
        * 共有三份副本，一份主线程，另启的线程各一个，其中的值互不干扰
        * */
        new MyTest(at, "1").start();
        new MyTest(at, "2").start();
    }
}
