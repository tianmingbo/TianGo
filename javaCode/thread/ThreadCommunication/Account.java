package thread.ThreadCommunication;

//线程通信
public class Account {
    private String accountNo;
    private double balance;
    private boolean flag = false;

    public Account(String accountNo, double balance) {
        this.accountNo = accountNo;
        this.balance = balance;
    }

    public Account() {
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

    public synchronized void draw(double drawAmount) {
        try {
            if (!flag) {
                wait(); //线程等待
            } else {
                System.out.println(Thread.currentThread().getName() + "get money:" + drawAmount);
                balance -= drawAmount;
                System.out.println("余额为：" + balance);
                flag = false;
                notifyAll(); //唤醒其他线程
            }
        } catch (InterruptedException ex) {
            ex.printStackTrace();
        }
    }

    public synchronized void deposit(double depositAmount) {
        try {
            if (flag) {
                wait();
            } else {
                System.out.println(Thread.currentThread().getName() + "add money:" + depositAmount);
                balance += depositAmount;
                System.out.println("余额为：" + balance);
                flag = true;
                notifyAll(); //唤醒其他线程
            }
        } catch (InterruptedException ex) {
            ex.printStackTrace();
        }
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
