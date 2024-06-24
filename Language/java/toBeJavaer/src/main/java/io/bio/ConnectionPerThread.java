package io.bio;


import io.Nio.sockerDemo.NioDemoConfig;
import util.Logger;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * 每个线程处理一个请求
 */
class ConnectionPerThread implements Runnable {
    @Override
    public void run() {
        try {
            ServerSocket serverSocket = new ServerSocket(NioDemoConfig.SOCKET_SERVER_PORT);
            Logger.info(" server is up:", NioDemoConfig.SOCKET_SERVER_PORT);

            while (!Thread.interrupted()) {
                //每接收一个客户端的socket连接， 创建一个线程， 进行阻塞式的读写
                Socket socket = serverSocket.accept();

                Handler handler = new Handler(socket);
                //创建新线程来handle
                //或者，使用线程池来处理
                new Thread(handler).start();
            }

        } catch (IOException ex) { /* 处理异常 */ }
    }

    static class Handler implements Runnable {
        final Socket socket;

        Handler(Socket s) {
            socket = s;
            Logger.info("连接的两个端口:", socket.getPort(), socket.getLocalPort());

        }

        @Override
        public void run() {
            while (true) {
                try {
                    byte[] input = new byte[NioDemoConfig.SERVER_BUFFER_SIZE];
                    /* 读取数据 */
                    socket.getInputStream().read(input);

                    Logger.info("收到：" + socket.getPort() +"     message: "+ new String(input));

                    /* 处理业务逻辑，获取处理结果 */
                    byte[] output = input;
                    /* 写入结果 */
                    socket.getOutputStream().write(output);
                } catch (IOException ex) { /*处理异常*/ }
            }
        }

    }

    public static void main(String[] args) {
        new ConnectionPerThread().run();
    }
}