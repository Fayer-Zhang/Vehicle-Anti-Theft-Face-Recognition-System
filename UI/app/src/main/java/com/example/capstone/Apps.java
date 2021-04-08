package com.example.capstone;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class Apps extends AppCompatActivity {
    FirebaseAuth fAuth;
    Button remote, thief;
    DatabaseReference reff;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_apps);
        fAuth = FirebaseAuth.getInstance();
        remote = (Button)findViewById(R.id.remote);
        thief = (Button)findViewById(R.id.thiefpicb);

        remote.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), remotecamera.class));
            }
        });

        thief.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), VThiefPictures.class));
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
