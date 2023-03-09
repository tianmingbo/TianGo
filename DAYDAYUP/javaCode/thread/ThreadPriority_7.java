package thread;

//线程优先级
public class ThreadPriority_7 extends Thread {
    public ThreadPriority_7(String name) {
        super(name);
    }

    @Override
    public void run() {
        for (var i = 0; i < 10; i++) {
            System.out.println(getName() + "priority:" + getPriority() + "," + "value:" + i);
        }
    }

    public static void main(String[] args) {
        Thread.currentThread().setPriority(NORM_PRIORITY);
        for (var i = 0; i < 30; i++) {
            if (i == 10) {
                var low = new ThreadPriority_7("low");
                low.start();
                System.out.println("start:" + low.getPriority());
                low.setPriority(Thread.MIN_PRIORITY);
            }
            if (i == 20) {
                var high = new ThreadPriority_7("high");
                high.start();
                System.out.println("20start:" + high.getPriority());
                high.setPriority(Thread.MAX_PRIORITY);
            }
        }

    }
}
