package thread;

//线程组
class MyThread extends Thread {
    public MyThread(String name) {
        super(name);
    }

    public MyThread(ThreadGroup group, String name) {
        super(group, name);
    }

    @Override
    public void run() {
        for (var i = 0; i < 20; i++) {
            System.out.println(getName() + " i:" + i);
        }
    }
}

public class ThreadGroupTest_13 {
    public static void main(String[] args) {
        ThreadGroup mainGroup = Thread.currentThread().getThreadGroup();
        System.out.println("main thread name:" + mainGroup.getName());//主线程组的名字
        System.out.println("is daemon?" + mainGroup.isDaemon()); //
        var tg = new ThreadGroup("new thread group"); //创建一个新线程组
        tg.setDaemon(true);
        new MyThread(tg,"tg 组线程").start();
    }
}
