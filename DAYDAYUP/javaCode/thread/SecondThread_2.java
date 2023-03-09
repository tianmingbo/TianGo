package thread;

//通过实现Runnable接口来创建类
public class SecondThread_2 implements Runnable {
    private int i;

    public void run() {
        for (; i < 100; i++) {
            System.out.println(Thread.currentThread().getName() + " " + i);
        }
    }

    public static void main(String[] args) {
        for (var i = 0; i < 100; i++) {
            System.out.println(Thread.currentThread().getName() + " " + i);
            if (i == 20) {
                var st = new SecondThread_2();
                new Thread(st, "new_thread1").start(); //两个线程共享实例变量i，调用start后，进入就绪状态
                new Thread(st, "new thread2").start();
            }
        }
    }
}
