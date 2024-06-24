package internet.d9_chat;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;

public class ServerReaderThread extends Thread{
    private Socket socket;
    public ServerReaderThread(Socket socket){
        this.socket = socket;
    }
    @Override
    public void run() {
        try {
            // 3、从socket通信管道中得到一个字节输入流
            InputStream is = socket.getInputStream();
            // 4、把字节输入流包装成缓冲字符输入流进行消息的接收
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            // 5、按照行读取消息
            String msg;
            while ((msg = br.readLine()) != null){
                System.out.println(socket.getRemoteSocketAddress() + "说了：: " + msg);
                // 把这个消息发给当前所有在线socket
                sendMsgToAll(msg);
            }
        } catch (Exception e) {
            System.out.println(socket.getRemoteSocketAddress() + "下线了！！！");
            // 从在线集合中抹掉本客户端socket
            ServerDemo2.onLineSockets.remove(socket);
        }
    }

    private void sendMsgToAll(String msg) {
        try {
            // 遍历全部的在线 socket给他们发消息
            for (Socket onLineSocket : ServerDemo2.onLineSockets) {
                // 除了自己的socket，其他socket我都发！！
                if(onLineSocket != socket){
                    PrintStream ps = new PrintStream(socket.getOutputStream());
                    ps.println(msg);
                    ps.flush();
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
