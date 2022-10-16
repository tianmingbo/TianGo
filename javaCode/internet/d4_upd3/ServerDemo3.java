package internet.d4_upd3;

import java.net.*;

/**
  接收端
 */
public class ServerDemo3 {
    public static void main(String[] args) throws Exception {
        System.out.println("=====服务端启动======");
        // 1、创建接收端对象：注册端口（人）
        MulticastSocket socket = new MulticastSocket(9898);

        // 注意：绑定组播地址（加群）
        socket.joinGroup(new InetSocketAddress(InetAddress.getByName("224.0.1.1") , 9898),
                NetworkInterface.getByInetAddress(InetAddress.getLocalHost()));

        // 2、创建一个数据包对象接收数据（韭菜盘子）
        byte[] buffer = new byte[1024 * 64];
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length);


        while (true) {
            // 3、等待接收数据。
            socket.receive(packet);
            // 4、取出数据即可
            // 读取多少倒出多少
            int len = packet.getLength();
            String rs = new String(buffer,0, len);
            System.out.println("收到了来自：" + packet.getAddress() +", 对方端口是" + packet.getPort() +"的消息：" + rs);
        }
    }
}
