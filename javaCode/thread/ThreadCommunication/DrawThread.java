package thread.ThreadCommunication;

//取款线程
public class DrawThread extends Thread {
    private final Account account;
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
