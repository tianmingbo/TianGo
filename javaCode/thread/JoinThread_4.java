package thread;
//join()方法，join会阻塞调用线程，直到被join的线程结束


public class JoinThread_4 extends Thread {
    public JoinThread_4(String name) {
        super(name); //设置线程名字
    }

    public void run() {
        for (var i = 0; i < 10; i++) {
            System.out.println(getName() + " " + i);
        }
    }

    public static void main(String[] args) throws Exception {
        new JoinThread_4("new thread").start();
        for (var i = 0; i < 10; i++) {
            if (i == 5) {
                var jt = new JoinThread_4("join thread");
                jt.start();
                jt.join();
            }
            System.out.println(Thread.currentThread().getName() + " " + i);
        }
    }
}
