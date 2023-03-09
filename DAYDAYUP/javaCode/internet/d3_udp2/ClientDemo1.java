package internet.d3_udp2;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Scanner;

/**
  发送端  多发 多收
 */
public class ClientDemo1 {
    public static void main(String[] args) throws Exception {
        System.out.println("=====客户端启动======");

        // 1、创建发送端对象：发送端自带默认的端口号
        DatagramSocket socket = new DatagramSocket(7777);

        Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.println("请说：");
            String msg = sc.nextLine();

            if("exit".equals(msg)){
                System.out.println("离线成功！");
                socket.close();
                break;
            }

            // 2、创建一个数据包对象封装数据
            byte[] buffer = msg.getBytes();
            DatagramPacket packet = new DatagramPacket( buffer, buffer.length,
                    InetAddress.getLocalHost() , 8888);

            // 3、发送数据出去
            socket.send(packet);
        }

    }
}
