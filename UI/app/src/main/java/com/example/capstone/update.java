package com.example.capstone;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;
import java.util.Map;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

public class update extends AppCompatActivity {
    private EditText firstname, lastname, phone, email;
    private Button save, cancel;
    FirebaseAuth fAuth;
    private boolean check;
    FirebaseFirestore fstore;
    String userID;
    int numOfDrivers;
    private String fn, ln, ph;
    DatabaseReference reff;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_update );

        firstname = (EditText) findViewById(R.id.fname2);
        lastname = (EditText) findViewById(R.id.lname2);
        phone = (EditText) findViewById(R.id.phone2);
        save = (Button) findViewById(R.id.adddriver2);
        cancel = (Button) findViewById(R.id.cancel2);

        fAuth = FirebaseAuth.getInstance();
        fstore = FirebaseFirestore.getInstance();

        userID = fAuth.getCurrentUser().getUid();

        save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                fn = firstname.getText().toString().trim();
                ln = lastname.getText().toString().trim();
                ph = phone.getText().toString().trim();

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


                DocumentReference documentReference = fstore.collection("users").document(userID);
                Map<String,Object> user = new HashMap<>();
                documentReference.update("First Name",fn);
                documentReference.update("Last Name",ln);
                documentReference.update("Phone Number",ph);
                documentReference.update(user).addOnSuccessListener(new OnSuccessListener<Void>() {
                    @Override
                    public void onSuccess(Void aVoid) {
                    }
                });
                reff = FirebaseDatabase.getInstance().getReference().child("signal");
                documentReference.get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
                    @Override
                    public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                        if (task.isSuccessful()) {
                            DocumentSnapshot document = task.getResult();
                            if (document != null) {
                                String e = document.getString("Email");
                                reff.child("4").child("E-Mail").setValue(e);
                            } else {
                                Log.d("LOGGER", "No such document");
                            }
                        } else {
                            Log.d("LOGGER", "get failed with ", task.getException());
                        }
                    }
                });
                reff.child("4").child("First Name").setValue(fn);
                reff.child("4").child("Last Name").setValue(ln);
                reff.child("4").child("Phone").setValue(ph);
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
        startActivity(new Intent(getApplicationContext(), Login.class));
        finish();
    }

    public void back(View view){
        startActivity(new Intent(getApplicationContext(), Drivers.class));
    }
}
