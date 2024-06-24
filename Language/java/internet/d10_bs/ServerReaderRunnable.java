package internet.d10_bs;

import java.io.PrintStream;
import java.net.Socket;

public class ServerReaderRunnable implements Runnable{
    private Socket socket;
    public ServerReaderRunnable(Socket socket){
        this.socket = socket;
    }
    @Override
    public void run() {
        try {
            // 浏览器 已经与本线程建立了Socket管道
            // 响应消息给浏览器显示
            PrintStream ps = new PrintStream(socket.getOutputStream());
            // 必须响应HTTP协议格式数据，否则浏览器不认识消息
            ps.println("HTTP/1.1 200 OK"); // 协议类型和版本 响应成功的消息！
            ps.println("Content-Type:text/html;charset=UTF-8"); // 响应的数据类型：文本/网页

            ps.println(); // 必须发送一个空行

            // 才可以响应数据回去给浏览器
            ps.println("<span style='color:red;font-size:90px'>《最牛的149期》 </span>");
            ps.close();
        } catch (Exception e) {
            System.out.println(socket.getRemoteSocketAddress() + "下线了！！！");
        }
    }
}
