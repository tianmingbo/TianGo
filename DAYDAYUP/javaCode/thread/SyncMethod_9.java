package thread;

//同步方法
class Account2 {
    private String accountNo;
    private double balance;

    public Account2(String accountNo, double balance) {
        this.accountNo = accountNo;
        this.balance = balance;
    }

    public Account2() {
    }

    public void setAccountNo(String accountNo) {
        this.accountNo = accountNo;
    }


    public double getBalance() {
        return balance;
    }

    public String getAccountNo() {
        return accountNo;
    }

    public boolean equals(Object o) {
        if (this == o) return true;
        if (o != null && o.getClass() == Account2.class) {
            var target = (Account2) o;
            return target.getAccountNo().equals(accountNo);
        }
        return false;
    }

    public int hashCode() {
        return accountNo.hashCode();
    }

    //提供一个线程安全的draw()方法来完成取钱操作
    public synchronized void draw(double drawAmount) {
        if (balance < drawAmount) {
            System.out.println("money don't enough");
        } else {
            System.out.println(Thread.currentThread().getName() + "get money:" + drawAmount);
            try {
                Thread.sleep(1);
            } catch (Exception e) {
                e.printStackTrace();
            }
            balance -= drawAmount;
            System.out.println("余额为：" + balance);
        }
    }
}

class Draw2 extends Thread {
    private final Account2 account;
    private double drawAmount;

    public Draw2(String name, Account2 account, double drawAmount) {
        super(name);
        this.account = account;
        this.drawAmount = drawAmount;
    }

    public void run() {
        account.draw(800);
    }
}

public class SyncMethod_9 {
    public static void main(String[] args) {
        var account = new Account2("1231444", 1000);
        new Draw2("1", account, 800).start();
        new Draw2("2", account, 800).start();
    }
}
