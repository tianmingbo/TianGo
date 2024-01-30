package io.Nio.sockerDemo;

import util.IOUtil;
import util.Logger;
import util.ThreadUtil;

import java.io.File;
import java.io.FileInputStream;
import java.net.InetSocketAddress;
import java.net.StandardSocketOptions;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.channels.SocketChannel;

public class Test {
    public void sendFile() {
        try {
            String srcPath = NioDemoConfig.SOCKET_SEND_FILE;
            File file = new File(srcPath);
            FileChannel fileChannel = new FileInputStream(file).getChannel();
            SocketChannel socketChannel = SocketChannel.open();
            socketChannel.setOption(StandardSocketOptions.TCP_NODELAY, true);//用于控制是否开启 Nagle 算法
            socketChannel.socket().connect(
                    new InetSocketAddress(NioDemoConfig.SOCKET_SERVER_IP
                            , NioDemoConfig.SOCKET_SERVER_PORT));
            socketChannel.configureBlocking(false);
            Logger.info("sendFile start");
            while (!socketChannel.finishConnect()) {
                Logger.info("connecting");
            }
            byte[] bytes = file.getName().getBytes();
            //发送文件名称长度
            ByteBuffer buffer = ByteBuffer.allocate(NioDemoConfig.SEND_BUFFER_SIZE);
            buffer.putInt(bytes.length);
            buffer.flip();
            socketChannel.write(buffer);
            Logger.info("client 文件名称长度发送完成:", bytes.length);
            //发送文件名
            socketChannel.write(ByteBuffer.wrap(bytes));
            Logger.info("文件名称发送完成:", file.getName());

            //发送文件长度
            buffer.clear();
            buffer.putInt((int) file.length());
            buffer.flip();
            socketChannel.write(buffer);
            Logger.info("文件长度发送完成:", file.length());

            Logger.info("开始传输文件");
            int length = 0;
            int offset = 0;
            buffer.clear();
            while ((length = fileChannel.read(buffer)) > 0) {
                buffer.flip();
                socketChannel.write(buffer);
                offset += length;
                Logger.debug("| " + (100 * offset / file.length()) + "% |");
                buffer.clear();
            }
            //等待一分钟关闭连接
            ThreadUtil.sleepSeconds(60);

            if (length == -1) {
                IOUtil.closeQuietly(fileChannel);
                //调用终止输出方法，向对方发送一个输出的结束标志
                socketChannel.shutdownOutput();
                //关闭套接字连接
                IOUtil.closeQuietly(socketChannel);
            }
            Logger.debug("======== 文件传输成功 ========");

        } catch (Exception e) {
            e.printStackTrace();

        }
    }

    public static void main(String[] args) {

    }
}
