package thread;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

//使用blockingQueue进行线程通信
class Producer extends Thread {
    private BlockingQueue<String> bq;

    public Producer(BlockingQueue<String> bq) {
        this.bq = bq;
    }

    public void run() {
        var strArr = new String[]{"Java", "py", "C++"};
        for (var i = 0; i < 10; i++) {
            System.out.println(getName() + "：producer");
            try {
                Thread.sleep(200);
                //放入元素，如果队列已满，陷入阻塞
                bq.put(strArr[i % 3]);
            } catch (InterruptedException ex) {
                ex.printStackTrace();
            }
            System.out.println(getName() + "：done" + bq);
        }
    }
}

class Consumer extends Thread {
    private BlockingQueue<String> bq;

    public Consumer(BlockingQueue<String> bq) {
        this.bq = bq;
    }

    public void run() {
        while (true) {
            System.out.println(getName() + "：Consumer");
            try {
                Thread.sleep(200);
                //取出元素，如果队列为空，陷入阻塞
                bq.take();
            } catch (InterruptedException ex) {
                ex.printStackTrace();
            }
            System.out.println(getName() + "：done" + bq);
        }
    }
}

public class BlockingQueueTest_12 {
    public static void main(String[] args) {
        //创建一个容量为1的阻塞队列
        BlockingQueue<String> bq = new ArrayBlockingQueue<>(1);
        //创建3个生产者
        new Producer(bq).start();
        new Producer(bq).start();
        new Producer(bq).start();
        //一个消费者
        new Consumer(bq).start();
    }
}
