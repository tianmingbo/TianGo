package thread;

import java.util.Date;

//线程睡眠
public class ThreadSleep_6 extends Thread {
    public static void main(String[] args) throws Exception {
        for (var i = 0; i < 10; i++) {
            System.out.println(new Date());
            Thread.sleep(1000);//暂停一秒
        }
    }
}
