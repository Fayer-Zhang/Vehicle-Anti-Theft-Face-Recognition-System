package com.example.capstone;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.MediaController;
import android.widget.VideoView;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class remotecamera extends AppCompatActivity {
    FirebaseAuth fAuth;
    WebView videoView;
    ImageButton btnPlayPause;
    DatabaseReference reff;
    int check = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_remotecamera);
        fAuth = FirebaseAuth.getInstance();
        videoView = (WebView) findViewById(R.id.remotecameravideo);
        btnPlayPause = (ImageButton)findViewById(R.id.btn_play_pause);
        reff = FirebaseDatabase.getInstance().getReference().child("signal");

        btnPlayPause.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (check == 0) {
                    reff.child("1").child("camera").setValue("on");
                    videoView.setWebViewClient(new WebViewClient());
                    videoView.loadUrl("http://lileyao1998.synology.me:15000");
                    videoView.getSettings().setLoadWithOverviewMode(true);
                    videoView.getSettings().setUseWideViewPort(true);
                    btnPlayPause.setImageResource(R.drawable.ic_play);
                    check = 1;
                } else {
                    btnPlayPause.setImageResource(R.drawable.ic_pause);
                    reff.child("1").child("camera").setValue("off");
                    check = 0;
                }
            }
        });
    }

    public void logout(View view){
        fAuth.signOut();
        reff = FirebaseDatabase.getInstance().getReference().child("signal");
        reff.child("1").child("camera").setValue("off");
        reff.child("1").child("power").setValue("off");
        reff.child("1").child("motor").setValue("off");
        reff.child("1").child("alarm").setValue("off");
        startActivity(new Intent(getApplicationContext(), Login.class));
        finish();
    }

    public void back(View view){
        startActivity(new Intent(getApplicationContext(), homepage.class));
    }

}
