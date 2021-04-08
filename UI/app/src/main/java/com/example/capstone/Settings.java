package com.example.capstone;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class Settings extends AppCompatActivity {
    FirebaseAuth fAuth;
    private Button dri, enr, sup, pas, abu;
    DatabaseReference reff;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        fAuth = FirebaseAuth.getInstance();

        dri = findViewById(R.id.managedrivers);
        enr = findViewById(R.id.enrollment);
        sup = findViewById(R.id.support);
        pas = findViewById(R.id.password);
        abu = findViewById(R.id.aboutus);

        dri.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), Drivers.class));
            }
        });

        enr.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), Enrollment.class));
            }
        });

        sup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), Support.class));
            }
        });

        pas.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), Password.class));
            }
        });

        abu.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), About.class));
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
