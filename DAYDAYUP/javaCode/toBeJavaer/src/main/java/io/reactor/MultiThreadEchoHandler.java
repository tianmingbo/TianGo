package io.reactor;


import util.Logger;

import java.io.IOException;
import java.net.StandardSocketOptions;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

class MultiThreadEchoHandler implements Runnable {
    final SocketChannel channel;
    final SelectionKey sk;
    final ByteBuffer byteBuffer = ByteBuffer.allocate(1024);
    static final int RECIEVING = 0, SENDING = 1;
    int state = RECIEVING;
    //引入线程池
    static ExecutorService pool = Executors.newFixedThreadPool(4);

    public MultiThreadEchoHandler(Selector selector, SocketChannel c) throws IOException {
        channel = c;
        channel.configureBlocking(false);
        channel.setOption(StandardSocketOptions.TCP_NODELAY, true);
        //仅仅取得选择键，后设置感兴趣的IO事件
        sk = channel.register(selector, 0);
        //将本Handler作为sk选择键的附件，方便事件dispatch
        sk.attach(this);
        //向sk选择键注册Read就绪事件
        sk.interestOps(SelectionKey.OP_READ);
        //唤醒 查询线程，使得OP_READ生效
        selector.wakeup();
        Logger.info("新的连接 注册完成");

    }

    @Override
    public void run() {
        //异步任务，在独立的线程池中执行
        //提交数据传输任务到线程池
        //使得IO处理不在IO事件轮询线程中执行，在独立的线程池中执行
        pool.execute(new AsyncTask());
    }

    //异步任务，不在Reactor线程中执行
    //数据传输与业务处理任务，不在IO事件轮询线程中执行，在独立的线程池中执行
    public synchronized void asyncRun() {
        try {
            if (state == SENDING) {
                //写入通道
                channel.write(byteBuffer);

                //写完后,准备开始从通道读,byteBuffer切换成写模式
                byteBuffer.clear();
                //写完后,注册read就绪事件
                sk.interestOps(SelectionKey.OP_READ);
                //写完后,进入接收的状态
                state = RECIEVING;
            } else if (state == RECIEVING) {
                //从通道读
                int length = 0;
                while ((length = channel.read(byteBuffer)) > 0) {
                    Logger.info(new String(byteBuffer.array(), 0, length));
                }
                //读完后，准备开始写入通道,byteBuffer切换成读模式
                byteBuffer.flip();
                //读完后，注册write就绪事件
                sk.interestOps(SelectionKey.OP_WRITE);
                //读完后,进入发送的状态
                state = SENDING;
            }
            //处理结束了, 这里不能关闭select key，需要重复使用
            //sk.cancel();
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    //异步任务的内部类
    class AsyncTask implements Runnable {
        @Override
        public void run() {
            MultiThreadEchoHandler.this.asyncRun();
        }
    }

}

