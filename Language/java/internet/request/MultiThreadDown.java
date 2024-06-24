package internet.request;

import java.io.InputStream;
import java.io.RandomAccessFile;
import java.net.HttpURLConnection;
import java.net.URL;

class DownUtil {
    private String path;
    private String targetFile;
    private int threadNum;
    private DownThread[] threads;
    private int fileSize;

    public DownUtil(String path, String targetFile, int threadNum) {
        this.path = path;
        this.targetFile = targetFile;
        threads = new DownThread[threadNum];
        this.threadNum = threadNum;
    }

    public double getCompleteRate() {
        int sumSize = 0;
        for (int i = 0; i < threadNum; i++) {
            sumSize += threads[i].length;
        }
        return sumSize * 1.0 / fileSize;
    }

    public void download() throws Exception {
        URL url = new URL(path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setConnectTimeout(5000);
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Accept", "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8");
        conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36");
        fileSize = conn.getContentLength();
        System.out.println("fileSize"+fileSize);
        conn.disconnect();
        int currentPartSize = fileSize / threadNum + 1;
        RandomAccessFile file = new RandomAccessFile(targetFile, "rw");
        file.setLength(fileSize);
        file.close();
        for (int i = 0; i < threadNum; i++) {
//            int startPos = i * currentPartSize;
            int startPos = 0;
            RandomAccessFile currentPart = new RandomAccessFile(targetFile, "rw");
            currentPart.seek(startPos);
            threads[i] = new DownThread(startPos, currentPartSize, currentPart);
            threads[i].start();
        }
    }

    private class DownThread extends Thread {
        private int startPos;
        private int currentPortSize;
        private RandomAccessFile currentPart;
        public int length;

        public DownThread(int startPos, int currentPortSize, RandomAccessFile currentPart) {
            this.startPos = startPos;
            this.currentPortSize = currentPortSize;
            this.currentPart = currentPart;
        }

        @Override
        public void run() {
            try {
                URL url = new URL(path);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setConnectTimeout(5000);
                conn.setRequestMethod("GET");
                conn.setRequestProperty("Accept", "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8");
                conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36");
                InputStream inStream = conn.getInputStream();
                inStream.skip(startPos);
                byte[] buf = new byte[1024];
                int hasRead = 0;
                while (length < currentPortSize && (hasRead = inStream.read()) != -1) {
                    currentPart.write(buf, 0, hasRead);
                    length += hasRead;
                }
                currentPart.close();
                inStream.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}

/**
 * @author tianmingbo
 */
public class MultiThreadDown {
    public static void main(String[] args) throws Exception {
        DownUtil util = new DownUtil("https://pic4.zhimg.com/v2-445c04e697de450ff21b7e50a005b0bf_r.jpg?source=1940ef5c", "tmp.jpg", 1);
        util.download();
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (util.getCompleteRate() < 1) {
                    System.out.println("已完成" + util.getCompleteRate());
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }
}