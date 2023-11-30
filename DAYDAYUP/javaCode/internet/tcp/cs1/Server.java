package internet.tcp.cs1;

import java.io.IOException;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * @author tianmingbo
 */
public class Server {
    public static void main(String[] args) throws IOException {
        ServerSocket ss = new ServerSocket(30000);
        System.out.println("start server");
        while (true){
            Socket s = ss.accept();
            System.out.println(s.getPort());
            System.out.println(s.getInetAddress());
            System.out.println(s);
            PrintStream ps = new PrintStream(s.getOutputStream());
            ps.println("666");
            ps.close();
//            ss.close();
        }
    }
}
