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
    private Button setting, poweron, alarmoff;
    DatabaseReference reff;
    Signal sig;
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
        at = findViewById(R.id.alarmtitle3);
        a = findViewById(R.id.alarm);
        et = findViewById(R.id.enginetitle3);
        e = findViewById(R.id.engine);

        reff = FirebaseDatabase.getInstance().getReference().child("signal");
        sig = new Signal();
        sig.setMotor("off");
        sig.setPower("off");
        sig.setAlarm("off");
        reff.child("1").setValue(sig);

        setting.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), Settings.class));
            }
        });

        poweron.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(check == 0){
                    sig.setPower("on");
                    sig.setMotor("on");
                    e.setImageResource(R.drawable.ic_power_on);
                    et.setText("ON");
                    check = 1;
                } else {
                    sig.setPower("off");
                    sig.setMotor("off");
                    e.setImageResource(R.drawable.ic_power_off);
                    et.setText("OFF");
                    check = 0;

                }
                reff.child("1").setValue(sig);
            }
        });

        alarmoff.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(check2 == 0){
                    sig.setAlarm("on");
                    a.setImageResource(R.drawable.ic_alarm_on);
                    at.setText("ON");
                    check2 = 1;
                } else {
                    sig.setAlarm("off");
                    a.setImageResource(R.drawable.ic_alarm_off);
                    at.setText("OFF");
                    check2 = 0;

                }
                reff.child("1").setValue(sig);
            }
        });

    }

    public void logout(View view){
        fAuth.signOut();
        startActivity(new Intent(getApplicationContext(), Login.class));
        finish();
    }
}
