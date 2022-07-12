package thread.ThreadCommunication;

public class TestClass {
    public static void main(String[] args) {
        var acct=new Account("12222",0);
        new DrawThread("geter",acct,800).start();
        new DepositThread("1",acct,800).start();
        new DepositThread("2",acct,800).start();
        new DepositThread("3",acct,800).start();
    }
}
