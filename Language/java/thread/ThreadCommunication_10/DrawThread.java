package thread.ThreadCommunication_10;

import thread.ThreadCommunication_11.Account;

//取款线程
public class DrawThread extends Thread {
    private final thread.ThreadCommunication_11.Account account;
    private double drawAmount;

    public DrawThread(String name, Account account, double drawAmount) {
        super(name);
        this.account = account;
        this.drawAmount = drawAmount;
    }

    public void run() {
        for (var i = 0; i < 100; i++) {
            account.draw(drawAmount);
        }
    }
}
