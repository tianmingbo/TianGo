package internet.d2_udp1;

import java.net.DatagramPacket;
import java.net.DatagramSocket;

/**
  接收端
 */
public class ServerDemo2 {
    public static void main(String[] args) throws Exception {
        System.out.println("=====服务端启动======");
        // 1、创建接收端对象：注册端口（人）
        DatagramSocket socket = new DatagramSocket(8888);

        // 2、创建一个数据包对象接收数据（韭菜盘子）
        byte[] buffer = new byte[1024 * 64];
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length);

        // 3、等待接收数据。
        socket.receive(packet);

        // 4、取出数据即可
        // 读取多少倒出多少
        int len = packet.getLength();
        String rs = new String(buffer,0, len);
        System.out.println("收到了：" + rs);

        // 获取发送端的ip和端口
        String ip  =packet.getSocketAddress().toString();
        System.out.println("对方地址：" + ip);

        int port  = packet.getPort();
        System.out.println("对方端口：" + port);

        socket.close();
    }
}
