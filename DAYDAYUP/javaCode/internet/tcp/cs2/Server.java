package internet.tcp.cs2;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

class ServerThread implements Runnable {
    Socket s = null;
    BufferedReader br = null;

    public ServerThread(Socket s) throws IOException {
        this.s = s;
        br = new BufferedReader(new InputStreamReader(s.getInputStream()));
    }

    @Override
    public void run() {
        try {
            String content = null;
            while ((content = readFromClient()) != null) {
                for (Socket s : Server.socketList) {
                    PrintStream ps = new PrintStream(s.getOutputStream());
                    ps.println(content);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    private String readFromClient() {
        try {
            return br.readLine();
        } catch (Exception e) {
            Server.socketList.remove(s);
        }
        return null;

    }
}

/**
 * @author tianmingbo
 */
public class Server {
    public static List<Socket> socketList = Collections.synchronizedList(new ArrayList<>());

    public static void main(String[] args) throws IOException {
        ServerSocket ss = new ServerSocket(3000);
        System.out.println("server start");
        while (true) {
            Socket s = ss.accept();
            socketList.add(s);
            System.out.println("add:" + s.getPort());
            new Thread(new ServerThread(s)).start();
        }
    }
}
