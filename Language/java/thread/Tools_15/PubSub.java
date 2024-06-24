package thread.Tools_15;

import java.util.List;
import java.util.concurrent.Flow.Subscription;
import java.util.concurrent.Flow.Subscriber;
import java.util.concurrent.SubmissionPublisher;

//发布订阅
class MySub<T> implements Subscriber<T> {
    private Subscription subscription;

    @Override
    public void onSubscribe(Subscription subscription) {
        this.subscription = subscription;
        subscription.request(1);
    }

    @Override
    public void onNext(T item) {
        System.out.println("get data:" + item);
        subscription.request(1);
    }

    @Override
    public void onError(Throwable throwable) {
        throwable.printStackTrace();
        synchronized ("fkjava") {
            "fkjava".notifyAll();
        }
    }

    @Override
    public void onComplete() {
        System.out.println("done");
        synchronized ("fkjava") {
            "fkjava".notifyAll();
        }
    }
}

public class PubSub {
    public static void main(String[] args) {
        //发布者
        SubmissionPublisher<String> publisher = new SubmissionPublisher<>();
        //订阅者
        MySub<String> sub = new MySub<>();
        //注册订阅者
        publisher.subscribe(sub);
        System.out.println("start pub data");
        List.of("java", "C++", "py", "C").forEach(im -> {
            //发布数据
            publisher.submit(im);
            try {
                Thread.sleep(500);
            } catch (Exception ignored) {

            }
        });
        //发布结束
        publisher.close();
        //发布结束后，暂停线程
        synchronized ("fkjava") {
            try {
                "fkjava".wait();
            } catch (Exception ignored) {
            }
        }
    }
}
