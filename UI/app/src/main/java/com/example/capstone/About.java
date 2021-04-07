package com.example.capstone;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import com.google.firebase.auth.FirebaseAuth;

public class About extends AppCompatActivity {
    FirebaseAuth fAuth;
    private TextView web;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_about);
        fAuth = FirebaseAuth.getInstance();
        web = findViewById(R.id.abouttitle3);

        web.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Uri uri = Uri.parse("https://sherm048.github.io/");
                startActivity(new Intent(Intent.ACTION_VIEW,uri));
            }
        });

    }

    public void logout(View view){
        fAuth.signOut();
        startActivity(new Intent(getApplicationContext(), Login.class));
        finish();
    }

    public void back(View view){
        startActivity(new Intent(getApplicationContext(), Settings.class));
    }
}
