package com.xjb.demo02;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;

import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    private String total = "hello";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        while (true) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            fun(50, 30);
            Log.d("tian", fun("run Me"));
        }
    }

    void fun(int x, int y) {
        Log.d("tian", String.valueOf(x + y));
    }

    String fun(String x) {
        return x.toLowerCase(Locale.ROOT);
    }

    void secret() {
        total += "secret";
        Log.d("tian secret", "this is a secret");
    }

    static void staticSecret() {
        Log.d("tian", "this is a static method");
    }

     void testIf(int b){
        int a=1;
        if(b<a){
            Log.d("tian","a is greater than b");
        }else{
            Log.d("tian","a is less than or equal b");
        }
    }
}
