package com.example.capstone;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.Toolbar;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.HashMap;

public class homepage extends AppCompatActivity {
    FirebaseAuth fAuth;
    private Button setting, poweron, alarmoff, apps;
    DatabaseReference reff;
    int check = 0;
    int check2 = 0;
    private ImageView a, e;
    private TextView at, et;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_homepage);
        fAuth = FirebaseAuth.getInstance();
        setting = findViewById(R.id.settings);
        poweron = findViewById(R.id.poweron);
        alarmoff = findViewById(R.id.alarmoff);
        apps = findViewById(R.id.apps);
        at = findViewById(R.id.alarmtitle3);
        a = findViewById(R.id.alarm);
        et = findViewById(R.id.enginetitle3);
        e = findViewById(R.id.engine);

        reff = FirebaseDatabase.getInstance().getReference().child("signal");
        reff.child("1").child("power").setValue("off");
        reff.child("1").child("motor").setValue("off");
        reff.child("1").child("alarm").setValue("off");

        setting.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), Settings.class));
            }
        });

        apps.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), Apps.class));
            }
        });


        poweron.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(check == 0){
                    reff.child("1").child("power").setValue("on");
                    e.setImageResource(R.drawable.ic_power_on);
                    et.setText("ON");
                    check = 1;
                } else {
                    reff.child("1").child("power").setValue("off");
                    e.setImageResource(R.drawable.ic_power_off);
                    et.setText("OFF");
                    check = 0;

                }
            }
        });

        alarmoff.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(check2 == 0){
                    reff.child("1").child("alarm").setValue("on");
                    a.setImageResource(R.drawable.ic_alarm_on);
                    at.setText("ON");
                    check2 = 1;
                } else {
                    reff.child("1").child("alarm").setValue("off");
                    a.setImageResource(R.drawable.ic_alarm_off);
                    at.setText("OFF");
                    check2 = 0;

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

    }

}
