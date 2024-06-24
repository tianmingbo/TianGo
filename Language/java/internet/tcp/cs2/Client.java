package internet.tcp.cs2;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;

class ClientThread implements Runnable {
    private Socket s;
    BufferedReader br;

    public ClientThread(Socket s) throws IOException {
        this.s = s;
        br = new BufferedReader(new InputStreamReader(s.getInputStream()));
    }

    @Override
    public void run() {
        try {
            String content;
            while ((content = br.readLine()) != null) {
                System.out.println(content);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

/**
 * @author tianmingbo
 */
public class Client {
    public static void main(String[] args) throws IOException {
        Socket s = new Socket("127.0.0.1", 3000);
        new Thread(new ClientThread(s)).start();
        PrintStream ps = new PrintStream(s.getOutputStream());
        String line;
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        while ((line = br.readLine()) != null) {
            ps.println(line);
        }
    }
}
