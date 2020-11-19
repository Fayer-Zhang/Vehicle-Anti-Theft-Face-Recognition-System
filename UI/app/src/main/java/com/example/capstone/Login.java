package com.example.capstone;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;

public class Login extends AppCompatActivity {
    private EditText email, password;
    private Button save;
    private TextView account;
    FirebaseAuth fAuth;
    private String em, pw;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        email = (EditText) findViewById(R.id.username);
        password = (EditText) findViewById(R.id.password);
        save = (Button) findViewById(R.id.signin);
        account = findViewById(R.id.account);
        fAuth = FirebaseAuth.getInstance();

        account.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), signup.class));
            }
        });

        save.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                em = email.getText().toString().trim();
                pw = password.getText().toString().trim();

                if(TextUtils.isEmpty(em)){
                    email.setError("Email is Required.");
                    return;
                }

                if(TextUtils.isEmpty(pw)){
                    password.setError("Email is Required.");
                    return;
                }

                fAuth.signInWithEmailAndPassword(em, pw).addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if(task.isSuccessful()){
                            Toast.makeText(Login.this, "Successful Login", Toast.LENGTH_LONG).show();
                            openHomepage();
                        } else {
                            Toast.makeText(Login.this, task.getException().toString(), Toast.LENGTH_LONG).show();
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
}
