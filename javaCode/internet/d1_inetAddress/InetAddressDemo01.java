package internet.d1_inetAddress;

import java.net.InetAddress;

/**
 * InetAddress类
 * 一个该类的对象就代表一个IP地址对象。
 * InetAddress类成员方法：
 * getLocalHost()
 * 获得本地主机IP地址对象。
 * getByName(String host)
 * 根据IP地址字符串或主机名获得对应的IP地址对象。
 * getHostName()
 * 获得主机名。
 * getHostAddress()
 * 获得IP地址字符串。
 */
public class InetAddressDemo01 {
    public static void main(String[] args) throws Exception {
        // 1.获取本机地址对象。
        InetAddress ip1 = InetAddress.getLocalHost();
        System.out.println(ip1.getHostName());
        System.out.println(ip1.getHostAddress());

        // 2.获取域名ip对象
        InetAddress ip2 = InetAddress.getByName("www.baidu.com");
        System.out.println(ip2.getHostName());
        System.out.println(ip2.getHostAddress());

        // 3.获取公网IP对象。
        InetAddress ip3 = InetAddress.getByName("112.80.248.76");
        System.out.println(ip3.getHostName());
        System.out.println(ip3.getHostAddress());

        // 4.判断是否能通： ping  5s之前测试是否可通
        System.out.println(ip3.isReachable(5000));
    }
}