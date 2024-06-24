package thread.ThreadCommunication_10;

import thread.ThreadCommunication_11.Account;
import thread.ThreadCommunication_11.DepositThread;
import thread.ThreadCommunication_11.DrawThread;

public class TestClass {
    public static void main(String[] args) {
        var acct = new Account("12222", 0);
        new DrawThread("geter", acct, 800).start();
        new thread.ThreadCommunication_11.DepositThread("1", acct, 800).start();
        new thread.ThreadCommunication_11.DepositThread("2", acct, 800).start();
        new DepositThread("3", acct, 800).start();
    }
}
