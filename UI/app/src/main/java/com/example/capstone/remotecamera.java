package com.example.capstone;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.VideoView;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class remotecamera extends AppCompatActivity {
    FirebaseAuth fAuth;
    ProgressDialog mDialog;
    VideoView videoView;
    ImageButton btnPlayPause;
    DatabaseReference reff;
    String videoURL = "http://llycanada.51vip.biz:15000";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_remotecamera);
        fAuth = FirebaseAuth.getInstance();
        videoView = (VideoView)findViewById(R.id.remotecameravideo);
        btnPlayPause = (ImageButton)findViewById(R.id.btn_play_pause);
        reff = FirebaseDatabase.getInstance().getReference().child("signal");

        btnPlayPause.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                reff.child("1").child("camera").setValue("on");
                mDialog = new ProgressDialog(remotecamera.this);
                mDialog.setMessage("Please wait...");
                mDialog.setCanceledOnTouchOutside(true);
                mDialog.show();

                try{
                    if(!videoView.isPlaying()) {
                        Uri uri = Uri.parse(videoURL);
                        videoView.setVideoURI(uri);
                        videoView.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                            @Override
                            public void onCompletion(MediaPlayer mp) {
                                btnPlayPause.setImageResource(R.drawable.ic_play);
                            }
                        });
                    } else {
                        videoView.pause();
                        btnPlayPause.setImageResource(R.drawable.ic_play);
                    }
                }catch (Exception ex){

                }
                videoView.requestFocus();
                videoView.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
                    @Override
                    public void onPrepared(MediaPlayer mp) {
                        mDialog.dismiss();
                        mp.setLooping(true);
                        videoView.start();
                        btnPlayPause.setImageResource(R.drawable.ic_pause);
                        reff.child("1").child("camera").setValue("off");
                    }
                });
            }
        });
    }

    public void logout(View view){
        fAuth.signOut();
        startActivity(new Intent(getApplicationContext(), Login.class));
        finish();
    }

    public void back(View view){
        startActivity(new Intent(getApplicationContext(), homepage.class));
    }
}
