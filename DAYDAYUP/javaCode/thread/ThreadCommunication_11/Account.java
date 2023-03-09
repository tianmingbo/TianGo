package thread.ThreadCommunication_11;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

//使用condition进行线程通信
public class Account {
    //lock对象
    private final Lock lock = new ReentrantLock();
    //Lock对象对应的Condition
    private final Condition cond = lock.newCondition();
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

    public void draw(double drawAmount) {
        lock.lock();
        try {
            if (!flag) {
                cond.await(); //线程等待
            } else {
                System.out.println(Thread.currentThread().getName() + "get money:" + drawAmount);
                balance -= drawAmount;
                System.out.println("余额为：" + balance);
                flag = false;
                cond.signalAll(); //唤醒其他线程
            }
        } catch (InterruptedException ex) {
            ex.printStackTrace();
        } finally {
            lock.unlock();
        }
    }

    public void deposit(double depositAmount) {
        lock.lock();
        try {
            if (flag) {
                cond.await();
            } else {
                System.out.println(Thread.currentThread().getName() + "add money:" + depositAmount);
                balance += depositAmount;
                System.out.println("余额为：" + balance);
                flag = true;
                cond.signalAll(); //唤醒其他线程
            }
        } catch (InterruptedException ex) {
            ex.printStackTrace();
        } finally {
            lock.unlock();
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
