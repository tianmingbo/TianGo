package com.xjb.http3demo;

import android.util.Log;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class example {
    private static final String TAG = "tian666";
    //创建一个客户端
    OkHttpClient client = new OkHttpClient();

    void run(String url) throws IOException {
        Request request = new Request.Builder().url(url).header("token", "tian").build();
        //enqueue产生一次真实的网络请求.发起异步请求
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                call.cancel();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                Log.d(TAG, response.body().string());
            }
        });
    }
}
