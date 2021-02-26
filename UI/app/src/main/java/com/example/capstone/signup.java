package com.example.capstone;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
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
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;

import java.util.HashMap;
import java.util.Map;

public class signup extends AppCompatActivity {
private EditText firstname, lastname, phone, email, password;
private Button save;
FirebaseAuth fAuth;
private TextView account;
private String fn, ln, em, pw, ph;
private boolean check, check2, check3, check4;
FirebaseFirestore fstore;
String userID;
DatabaseReference reff, sigR;
private String uCount;

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
                    phone.setError("Invalid phone number length");
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
                    password.setError("Password must be minumum of 6 characters.");
                    return;
                }

                check2 = FindUpperCase(pw);
                if(!check2){
                    password.setError("Password must contain one uppercase letter");
                    return;
                }

                check3 = FindNumber(pw);
                if(!check3){
                    password.setError("Password must contain one number");
                    return;
                }

                check4 = FindSpecialCharacter(pw);
                if(!check4){
                    password.setError("Password must contain one special character");
                    return;
                }
                fAuth.createUserWithEmailAndPassword(em, pw).addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if(task.isSuccessful()){
                            FirebaseUser fuser = fAuth.getCurrentUser();
                            fuser.sendEmailVerification().addOnSuccessListener(new OnSuccessListener<Void>() {
                                public void onSuccess(Void aVoid) {
                                    Toast.makeText(signup.this, "Successful Registration. Verification Email has been sent.", Toast.LENGTH_SHORT).show();
                                }
                            }).addOnFailureListener(new OnFailureListener() {
                                @Override
                                public void onFailure(@NonNull Exception e) {
                                    Toast.makeText(signup.this, "Please use valid Email address", Toast.LENGTH_SHORT).show();
                                }
                            });
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

                            reff = FirebaseDatabase.getInstance().getReference().child("signal");

                            /*DocumentReference noteRef = fstore.document("UserNum/Num");
                            noteRef.addSnapshotListener(new EventListener<DocumentSnapshot>() {
                                @Override
                                public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {
                                    if (value.exists()) {
                                        uCount = value.getString("UNum");
                                    }
                                }
                            });
                            Map<String, Object> note = new HashMap<>();
                            note.put("UNum", String.valueOf(uCount+1));
                            noteRef.set(note);*/

                            reff.child("2").child("E-Mail").setValue(em);
                            reff.child("2").child("First Name").setValue(fn);
                            reff.child("2").child("Last Name").setValue(ln);
                            reff.child("2").child("Phone").setValue(ph);

                            openEmail();
                        } else {
                            Toast.makeText(signup.this, task.getException().toString(), Toast.LENGTH_LONG).show();
                        }
                    }
                });
            }
        });
    }

    public void openEmail() {
        Intent intent = new Intent(this, Email.class);
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

    public static boolean FindUpperCase(String str){
        int count = 0;
        for(int i = 0; i<str.length(); i++){
            if(Character.isUpperCase(str.charAt(i))){
                count++;
            }
        }
        if(count >= 1){
            return true;
        } else {
            return false;
        }
    }

    public static boolean FindNumber(String str){
        int count = 0;
        for(int i = 0; i<str.length(); i++){
            if(Character.isDigit(str.charAt(i))){
                count++;
            }
        }
        if(count >= 1){
            return true;
        } else {
            return false;
        }
    }

    public boolean FindSpecialCharacter(String s) {
        Pattern p = Pattern.compile("[^A-Za-z0-9]");
        Matcher m = p.matcher(s);
        boolean b = m.find();
        return b;
    }
}
