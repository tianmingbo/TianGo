package io.reactor;


import io.Nio.sockerDemo.NioDemoConfig;
import util.Logger;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

/**
 * 单线程reactor模式
 */
class EchoServerReactor {
    private final ServerSocketChannel serverSocketChannel;
    private final Selector selector;

    EchoServerReactor() throws IOException {
        serverSocketChannel = ServerSocketChannel.open();
        serverSocketChannel.configureBlocking(false);
        serverSocketChannel.socket().bind(new InetSocketAddress(NioDemoConfig.SOCKET_SERVER_IP, NioDemoConfig.SOCKET_SERVER_PORT));
        selector = Selector.open();
        SelectionKey selectionKey = serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);
        selectionKey.attach(new Acceptor());

    }

    public void run() throws IOException {
        while (true) {
            selector.select(); //监听IO事件
            Iterator<SelectionKey> selectionKeys = selector.selectedKeys().iterator();
            while (selectionKeys.hasNext()) {
                SelectionKey selectionKey = selectionKeys.next();
                selectionKeys.remove();
                if (selectionKey.isAcceptable()) {
                    //连接请求到达
                    ((Acceptor) selectionKey.attachment()).accept();
                } else if (selectionKey.isReadable()) {
                    //读事件到达
                    ((Handler) selectionKey.attachment()).read();
                } else if (selectionKey.isWritable()) {
                    //写事件到达
                    ((Handler) selectionKey.attachment()).write();
                }
            }
        }
    }

    class Acceptor {
        public void accept() throws IOException {
            SocketChannel socketChannel = serverSocketChannel.accept();
            socketChannel.configureBlocking(false);
            Logger.info("accept: ", socketChannel.getRemoteAddress());
            Handler handler = new Handler(socketChannel);
            socketChannel.register(selector, SelectionKey.OP_READ, handler);
        }
    }

    class Handler {
        private final SocketChannel socketChannel;
        private final ByteBuffer readBuffer = ByteBuffer.allocate(1024);
        private final ByteBuffer writeBuffer = ByteBuffer.allocate(1024);


        public Handler(SocketChannel socketChannel) throws IOException {
            this.socketChannel = socketChannel;
        }

        public void read() throws IOException {
            readBuffer.clear();
            int bytesReadLength = socketChannel.read(readBuffer);
            if (bytesReadLength == -1) {
                socketChannel.close();
            } else if (bytesReadLength > 0) {
                Logger.info("read: ", new String(readBuffer.array(), 0, bytesReadLength));
                readBuffer.flip();
                writeBuffer.clear();
                writeBuffer.put(readBuffer);
                writeBuffer.flip();
                socketChannel.register(selector, SelectionKey.OP_WRITE, this);
            }

        }

        public void write() throws IOException {
            socketChannel.write(writeBuffer);
            if (!writeBuffer.hasRemaining()) {
                socketChannel.register(selector, SelectionKey.OP_READ, this);
            }
        }
    }

    public static void main(String[] args) throws IOException {
        Logger.info("start server:  ", NioDemoConfig.SOCKET_SERVER_IP, NioDemoConfig.SOCKET_SERVER_PORT);
        new EchoServerReactor().run();
    }

}
