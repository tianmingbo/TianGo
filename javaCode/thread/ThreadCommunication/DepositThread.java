package thread.ThreadCommunication;

public class DepositThread extends Thread {
    private Account account;
    private double depositAmount;

    public DepositThread(String name, Account account, double depositAmount) {
        super(name);
        this.account = account;
        this.depositAmount = depositAmount;
    }

    public void run() {
        for (var i = 0; i < 100; i++) {
            //重复100次存款
            account.deposit(depositAmount);
        }
    }
}
