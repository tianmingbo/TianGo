package thread.ThreadPool_14;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ThreadPoolTest_14 {
    public static void main(String[] args) {
        ExecutorService pool = Executors.newFixedThreadPool(5); //创建线程池
        //创建runnable对象
        Runnable target = () -> {
            for (var i = 0; i < 100; i++) {
                System.out.println(Thread.currentThread().getName() + " i value: " + i);
            }
        };
        //向线程池中加入两个线程
        pool.submit(target);
        pool.submit(target);
        //关闭线程池
        pool.shutdown();
    }
}
