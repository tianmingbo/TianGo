package internet.tcp.cs1;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetSocketAddress;
import java.net.Socket;

/**
 * @author tianmingbo
 */
public class Client {
    public static void main(String[] args) throws IOException {
//        Socket s = new Socket("127.0.0.1", 30000);
        Socket s = new Socket();
        s.connect(new InetSocketAddress(3000), 100000); //设置连接超时时间
        BufferedReader br = new BufferedReader(new InputStreamReader(s.getInputStream()));
        String line = br.readLine();
        System.out.println("from server:" + line);
        br.close();
        s.close();
    }
}
