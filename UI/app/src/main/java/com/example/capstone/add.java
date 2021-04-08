package com.example.capstone;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;

import java.util.HashMap;
import java.util.Map;

public class add extends AppCompatActivity {
    private EditText firstname, lastname, phone, email;
    private Button save, cancel;
    FirebaseAuth fAuth;
    private boolean check;
    FirebaseFirestore fstore;
    String userID;
    int numOfDrivers;
    private String fn, ln, em, ph;
    DatabaseReference reff;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add);

        firstname = (EditText) findViewById(R.id.fname);
        lastname = (EditText) findViewById(R.id.lname);
        phone = (EditText) findViewById(R.id.phone);
        email = (EditText) findViewById(R.id.email);
        save = (Button) findViewById(R.id.adddriver);
        cancel = (Button) findViewById(R.id.cancel);

        fAuth = FirebaseAuth.getInstance();
        fstore = FirebaseFirestore.getInstance();

        userID = fAuth.getCurrentUser().getUid();

        DocumentReference documentReference = fstore.collection("users").document(userID);

        documentReference.addSnapshotListener(this, new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {

                String test = value.getString("Number of Drivers");
                numOfDrivers = Integer.parseInt(test);
            }
        });

        save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                fn = firstname.getText().toString().trim();
                ln = lastname.getText().toString().trim();
                ph = phone.getText().toString().trim();
                em = email.getText().toString().trim();

                if(TextUtils.isEmpty(fn)){
                    firstname.setError("First name is Required.");
                    return;
                }

                if(TextUtils.isEmpty(ln)){
                    lastname.setError("Last name is Required.");
                    return;
                }

                if(TextUtils.isEmpty(ph)){
                    phone.setError("Phone number is Required.");
                    return;
                }

                check = onlyDigits(ph, ph.length());
                if(!check){
                    phone.setError("Invalid phone number");
                    return;
                }

                if(ph.length() < 10){
                    phone.setError("Invalid phone number");
                    return;
                }

                if(TextUtils.isEmpty(em)){
                    email.setError("Email is Required.");
                    return;
                }

                numOfDrivers++;

                DocumentReference documentReference = fstore.collection("users").document(userID);
                Map<String,Object> user = new HashMap<>();
                user.put("First Name"+String.valueOf(numOfDrivers),fn);
                user.put("Last Name"+String.valueOf(numOfDrivers),ln);
                user.put("Email"+String.valueOf(numOfDrivers),em);
                user.put("Phone Number"+String.valueOf(numOfDrivers),ph);
                user.put("Number of Drivers",String.valueOf(numOfDrivers));
                documentReference.update(user).addOnSuccessListener(new OnSuccessListener<Void>() {
                    @Override
                    public void onSuccess(Void aVoid) {
                    }
                });

                reff = FirebaseDatabase.getInstance().getReference().child("signal");
                reff.child("2").child("E-Mail").setValue(em);
                reff.child("2").child("First Name").setValue(fn);
                reff.child("2").child("Last Name").setValue(ln);
                reff.child("2").child("Phone").setValue(ph);
                openDriver();
            }
        });

        cancel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), Drivers.class));
            }
        });
    }

    public void openDriver() {
        Intent intent = new Intent(this, Drivers.class);
        startActivity(intent);
    }

    public static boolean onlyDigits(String str, int n) {
        for(int i = 0; i < n; i++) {
            if(str.charAt(i) >= '0'
                    && str.charAt(i) <= '9') {
                return true;
            } else {
                return false;
            }
        }
        return false;
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
        startActivity(new Intent(getApplicationContext(), Drivers.class));
    }
}
