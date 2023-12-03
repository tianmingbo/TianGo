package internet.tcp.cs2;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.*;

class ClientManager<K, V> {
    public Map<K, V> map = Collections.synchronizedMap(new HashMap<>());

    public synchronized void removeByValue(Object value) {
        for (K k : map.keySet()) {
            if (map.get(k) == value || map.get(k).equals(value)) {
                map.remove(k);
                break;
            }
        }
    }

    public synchronized Set<V> valueSet() {
        return new HashSet<>(map.values());
    }

    public synchronized K getKeyByValue(V val) {
        for (K k : map.keySet()) {
            if (map.get(k) == val || map.get(k).equals(val)) {
                return k;
            }
        }
        return null;
    }

    public synchronized V put(K key, V value) {
        return map.put(key, value);
    }
}

class ServerThread implements Runnable {
    private Socket s;
    BufferedReader br;
    PrintStream ps;

    public ServerThread(Socket s) {
        this.s = s;
    }

    @Override
    public void run() {
        try {
            //输入流
            BufferedReader br = new BufferedReader(new InputStreamReader(s.getInputStream()));
            //输出流
            PrintStream ps = new PrintStream(s.getOutputStream());
            String line;
            Server.clients.put(String.valueOf(s.getPort()), ps);
            while ((line = br.readLine()) != null) {
                //私聊
                if (line.startsWith(Protocol.PRIVATE_MSG) && line.endsWith(Protocol.PRIVATE_MSG)) {
                    String msg = getRealMsg(line);
                    String[] realMsg = msg.split("}}");
                    Server.clients.map.get(realMsg[1]).println(
                            Server.clients.getKeyByValue(ps) + "say you" + realMsg[2]
                    );
                } else {
                    String realMsg = getRealMsg(line);
                    System.out.println(realMsg + Server.clients.getKeyByValue(ps));
                    for (PrintStream clientPs : Server.clients.valueSet()) {
                        clientPs.println(Server.clients.getKeyByValue(ps) + "say: " + realMsg);
                    }
                }
            }
        } catch (Exception e) {
            Server.clients.removeByValue(ps);
            e.printStackTrace();
        }

    }

    private String getRealMsg(String msg) {
        return msg.substring(Protocol.PROTO_LEN, msg.length() - Protocol.PROTO_LEN);
    }
}

/**
 * @author tianmingbo
 */
public class Server {
    static int serverPort = 3000;
    static ClientManager<String, PrintStream> clients = new ClientManager<>();

    public void init() {
        try (ServerSocket ss = new ServerSocket(serverPort)) {
            System.out.println("server start");
            while (true) {
                Socket s = ss.accept();
                System.out.println("add:" + s.getPort());
                new Thread(new ServerThread(s)).start();
            }
        } catch (Exception e) {
            System.out.println("run error");
        }
    }

    public static void main(String[] args) throws IOException {
        Server server = new Server();
        server.init();
    }
}
