package thread;

import java.util.concurrent.Callable;
import java.util.concurrent.FutureTask;

//使用Callable和Future创建线程
public class ThirdThread_3 {
    public static void main(String[] args) {
//        var rt = new ThirdThread_3();
        //先使用lambda表达式创建Callable<Integer>对象
        //再使用FutureTask来包装Callable对象
        FutureTask<Integer> task = new FutureTask<>((Callable<Integer>) () -> {
            var i = 0;
            for (; i < 100; i++) {
                System.out.println(Thread.currentThread().getName() + " " + i);
            }
            return i;
        });
        for (var i = 0; i < 100; i++) {
            System.out.println(Thread.currentThread().getName() + " " + i);
            if (i == 20) {
                new Thread(task, "have return value").start();
            }
        }
        try {
            System.out.println("return value:" + task.get());
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
