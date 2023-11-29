package internet.request;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.URL;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;

/**
 * @author tianmingbo
 */
public class GetPost {
    public static String get(String url, String param) throws IOException {
        StringBuilder res = new StringBuilder();
        String path = url + "?" + param;
        try {
            URL url1 = new URL(path);
            URLConnection conn = url1.openConnection();
            conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36");
            conn.setRequestProperty("connection", "Keep-Alive");
            conn.connect();
            Map<String, List<String>> headers = conn.getHeaderFields();
            for (String s : headers.keySet()) {
                System.out.println(s + "---->" + headers.get(s));
            }
            try (BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = in.readLine()) != null) {
                    res.append("\n").append(line);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return res.toString();
    }

    public static String post(String url, String body) throws Exception {
        URL url1 = new URL(url);
        StringBuilder res = new StringBuilder();
        HttpURLConnection conn = (HttpURLConnection) url1.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json; utf-8");
        conn.setRequestProperty("Accept", "application/json");
        conn.setDoOutput(true);

        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = body.getBytes(StandardCharsets.UTF_8);
            os.write(input, 0, input.length);
        }

        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = br.readLine()) != null) {
                res.append(line.trim());
            }
        }
        return res.toString();
    }

    public static void main(String[] args) throws Exception {
        String s = GetPost.get("http://127.0.0.1:8000", "item_id=1");
        System.out.println(s);
        String posted = GetPost.post("http://127.0.0.1:8000/items/", "{\"name\":\"dali\"}");
        System.out.println(posted);
    }
}
