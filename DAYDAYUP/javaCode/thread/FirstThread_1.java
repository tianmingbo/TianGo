package thread;

//继承Thread来创建线程
public class FirstThread_1 extends Thread {
    private int i;

    //线程执行入口
    public void run() {
        for (; i < 100; i++) {
            System.out.println(getName() + " " + i);
        }
    }

    public static void main(String[] args) {
        for (var i = 0; i < 100; i++) {
            System.out.println(Thread.currentThread().getName() + " " + i);
            if (i == 20) {
                new FirstThread_1().start(); //创建线程并启动,因为每次启动都新建FirstThread_1对象，所以线程之间i变量不共享
                new FirstThread_1().start();
            }
        }
    }
}
