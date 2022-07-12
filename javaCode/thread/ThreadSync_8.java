package thread;

import java.util.Objects;

//线程同步，代码块同步
class Account {
    private String accountNo;
    private double balance;

    public Account(String accountNo, double balance) {
        this.accountNo = accountNo;
        this.balance = balance;
    }

    public Account() {
    }

    public void setAccountNo(String accountNo) {
        this.accountNo = accountNo;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }


    public double getBalance() {
        return balance;
    }

    public String getAccountNo() {
        return accountNo;
    }

    public boolean equals(Object o) {
        if (this == o) return true;
        if (o != null && o.getClass() == Account.class) {
            var target = (Account) o;
            return target.getAccountNo().equals(accountNo);
        }
        return false;
    }

    public int hashCode() {
        return accountNo.hashCode();
    }
}

class Draw extends Thread {
    private final Account account;
    private double drawAmount;

    public Draw(String name, Account account, double drawAmount) {
        super(name);
        this.account = account;
        this.drawAmount = drawAmount;
    }

    //多个线程同时修改共享变量是，会存在同步问题
    public void run() {
        /*
         *使用account作为同步监视器，任何线程在进入同步代码块之前，需要先获取account的锁，其他线程无法获得锁
         * */
        synchronized (account) {
            if (account.getBalance() >= drawAmount) {
                System.out.println("get:" + drawAmount);
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                account.setBalance(account.getBalance() - drawAmount);
                System.out.println("余额为：" + account.getBalance());
            } else {
                System.out.println(getName() + "余额不足");
            }
        }//结束释放锁

    }
}

public class ThreadSync_8 {
    public static void main(String[] args) {
        var account = new Account("1231444", 1000);
        new Draw("1", account, 800).start();
        new Draw("2", account, 800).start();
    }
}
