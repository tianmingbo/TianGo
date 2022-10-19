package internet;

import java.io.IOException;
import java.net.InetAddress;


//InetAddress代表一个ip地址对象
public class InetAddressTest_1 {
    public static void main(String[] args) throws IOException {
        InetAddress ip = InetAddress.getByName("www.baidu.com");
        System.out.println(ip.isReachable(2000)); //判断是否可达
        System.out.println(ip.getHostAddress()); //ip地址
        InetAddress local = InetAddress.getByAddress(new byte[]{120, 101, 49, 11});
        System.out.println(local.isReachable(2000));
        System.out.println(local.getCanonicalHostName());
    }
}
