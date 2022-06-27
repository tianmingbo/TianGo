package com.xjb.demo02;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;

import java.util.Locale;

public class MainActivity extends AppCompatActivity {

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
            fun(50, 20);
            Log.d("tian:", fun("SOULGOODMAN"));
        }
    }

    void fun(int a, int b) {
        Log.d("tian", String.valueOf(a + b));
    }

    String fun(String x) {
        return x.toLowerCase();
    }

    void secret() {
        Log.d("tian void", "this is instance func");
    }
    //类方法
    static void staticSecret() {
        Log.d("tian void", "this is class method");
    }
}