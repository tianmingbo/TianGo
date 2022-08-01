package com.xjb.httpurlconnection;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        new Thread(new Runnable() {

            @Override
            public void run() {
                while (true) {
                    try {
                        URL url = new URL("https://www.baidu.com");
                        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                        connection.setRequestMethod("GET");
                        connection.setRequestProperty("token", "tian666");
                        connection.setConnectTimeout(8000);
                        connection.setReadTimeout(8000);
                        connection.connect(); // 开始连接
                        InputStream in = connection.getInputStream(); //获取服务器的输入流
                        //if(in.available() > 0){

                        // 每次写入1024字节
                        int bufferSize = 1024;
                        byte[] buffer = new byte[bufferSize];
                        StringBuffer sb = new StringBuffer();
                        while ((in.read(buffer)) != -1) {
                            sb.append(new String(buffer));
                        }
                        Log.d("tian666", sb.toString());
                        connection.disconnect(); //断开连接
                        // }

                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    try {
                        Thread.sleep(10 * 1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
    }
}