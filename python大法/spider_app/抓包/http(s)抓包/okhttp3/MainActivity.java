package com.xjb.http3demo;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {
    private static String TAG = "tian666";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button btn = findViewById(R.id.mybtn);
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String requestUrl = "https://www.baidu.com";
                example myExample = new example();
                try {
                    myExample.run(requestUrl);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    }
}