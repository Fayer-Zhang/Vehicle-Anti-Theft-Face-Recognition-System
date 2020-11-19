package com.example.capstone;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Button;

import android.os.Bundle;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;
import java.util.Map;

public class signup extends AppCompatActivity {
private EditText firstname, lastname, phone, email, password;
private Button save;
FirebaseAuth fAuth;
private TextView account;
private String fn, ln, em, pw, ph;
private boolean check;
FirebaseFirestore fstore;
String userID;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        firstname = (EditText) findViewById(R.id.Fname);
        lastname = (EditText) findViewById(R.id.Lname);
        phone = (EditText) findViewById(R.id.phone);
        email = (EditText) findViewById(R.id.username);
        password = (EditText) findViewById(R.id.password);
        save = (Button) findViewById(R.id.siup);
        fAuth = FirebaseAuth.getInstance();
        account = findViewById(R.id.account1);
        fstore = FirebaseFirestore.getInstance();
        account.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), Login.class));
            }
        });

        save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                fn = firstname.getText().toString().trim();
                ln = lastname.getText().toString().trim();
                ph = phone.getText().toString().trim();
                em = email.getText().toString().trim();
                pw = password.getText().toString().trim();

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

                if(TextUtils.isEmpty(pw)){
                    password.setError("Password is Required.");
                    return;
                }

                if(pw.length() < 6){
                    password.setError("Password must be more than 6 characters.");
                    return;
                }

                fAuth.createUserWithEmailAndPassword(em, pw).addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if(task.isSuccessful()){
                            Toast.makeText(signup.this, "Successful Registration", Toast.LENGTH_LONG).show();
                            userID = fAuth.getCurrentUser().getUid();
                            DocumentReference documentReference = fstore.collection("users").document(userID);
                            Map<String,Object> user = new HashMap<>();
                            user.put("First Name",fn);
                            user.put("Last Name",ln);
                            user.put("Email",em);
                            user.put("Phone Number",ph);
                            user.put("Number of Drivers",String.valueOf(1));
                            documentReference.set(user).addOnSuccessListener(new OnSuccessListener<Void>() {
                                @Override
                                public void onSuccess(Void aVoid) {
                                }
                            });
                            openHomepage();
                        } else {
                            Toast.makeText(signup.this, task.getException().toString(), Toast.LENGTH_LONG).show();
                        }
                    }
                });
            }
        });
    }

    public void openHomepage() {
        Intent intent = new Intent(this, homepage.class);
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
}
