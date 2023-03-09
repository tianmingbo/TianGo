package thread;

//守护线程，前台线程死亡后，后台线程自动死亡
public class DaemonThread_5 extends Thread {
    public void run() {
        for (var i = 0; i < 999; i++) {
            System.out.println(getName() + " " + i);
        }
    }

    public static void main(String[] args) {
        var t = new DaemonThread_5();
        //设置成守护线程
        t.setDaemon(true);
        //判断是否是后台线程
        System.out.println(t.isDaemon());
        //启动后台线程
        t.start();
        for (var i = 0; i < 10; i++) {
            //后台线程不会输出到999，以为主线程先结束了，后台线程随之结束
            System.out.println(Thread.currentThread().getName() + " " + i);
        }
    }
}
