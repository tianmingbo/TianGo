package thread.ThreadPool_14;

import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;
import java.util.concurrent.TimeUnit;

//使用forkjoinPool利用多核
//RecursiveAction 没有返回值
class PrintTask extends RecursiveAction {
    private static final int Threshold = 50;
    private int start;
    private int end;

    public PrintTask(int start, int end) {
        this.start = start;
        this.end = end;
    }

    @Override
    protected void compute() {
        if (end - start < Threshold) {
            for (var i = start; i < end; i++) {
                System.out.println(Thread.currentThread().getName() + " i value: " + i);
            }
        } else {
            //当end-start>50时，开启多个子线程
            int middle = (start + end) / 2;
            var left = new PrintTask(start, middle);
            var right = new PrintTask(middle, end);
            //并行执行
            left.fork();
            right.fork();
        }
    }
}

public class ForkJoinPoolTest {
    public static void main(String[] args) throws Exception {
        var pool = new ForkJoinPool();
        pool.submit(new PrintTask(0, 300));
        pool.awaitTermination(2, TimeUnit.SECONDS);
        //关闭线程池
        pool.shutdown();
    }

}
