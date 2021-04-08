package com.example.capstone;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FieldValue;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Drivers extends AppCompatActivity{
    FirebaseAuth fAuth;
    FirebaseFirestore fstore;
    String userID;
    private RecyclerView mRecyclerView;
    private eAdapter mAdapter;
    private RecyclerView.LayoutManager mLayoutManager;
    ArrayList<driveritem> mExampleList = new ArrayList<>();
    private Button add, remove, update;
    String Fname, email, phone;
    int numOfDrivers;
    int removeP;
    DatabaseReference reff;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_drivers);
        fAuth = FirebaseAuth.getInstance();
        fstore = FirebaseFirestore.getInstance();
        add = findViewById(R.id.adddriver);
        remove = findViewById(R.id.removedriver);
        update = findViewById(R.id.updatedriver);

        userID = fAuth.getCurrentUser().getUid();

        DocumentReference documentReference = fstore.collection("users").document(userID);

        documentReference.addSnapshotListener(this, new EventListener<DocumentSnapshot>() {
            @Override
            public void onEvent(@Nullable DocumentSnapshot value, @Nullable FirebaseFirestoreException error) {

                String test = value.getString("Number of Drivers");
                numOfDrivers = Integer.parseInt(test);

                Fname = value.getString("First Name") + " " + value.getString("Last Name");
                email = value.getString("Email");
                phone = value.getString("Phone Number");
                mExampleList.add(new driveritem(Fname, email, phone));

                for(int i=1; i<numOfDrivers; i++){
                    Fname = value.getString("First Name"+(i+1)) + " " + value.getString("Last Name"+(i+1));
                    email = value.getString("Email"+(i+1));
                    phone = value.getString("Phone Number"+(i+1));
                    mExampleList.add(new driveritem(Fname, email, phone));
                }

                mRecyclerView = findViewById(R.id.recyclerview);
                mRecyclerView.setHasFixedSize(true);
                mLayoutManager = new LinearLayoutManager(Drivers.this);
                mAdapter = new eAdapter(mExampleList);
                mRecyclerView.setLayoutManager(mLayoutManager);
                mRecyclerView.setAdapter(mAdapter);

                mAdapter.setOnItemClickListener(new eAdapter.OnItemClickListener() {
                    @Override
                    public void onItemClick(int position) {
                        removeP = position;
                    }
                });
            }
        });

        add.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                addDriver();
            }
        });

        remove.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                removeDriver();
            }
        });

        update.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                updateDriver();
            }
        });

    }

    public void addDriver(){
        startActivity(new Intent(getApplicationContext(), add.class));
    }

    public void removeDriver(){
        if(removeP != 0){
            Map<String,Object> user = new HashMap<>();
            DocumentReference documentReference = fstore.collection("users").document(userID);
            documentReference.get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
                @Override
                public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                    if (task.isSuccessful()) {
                        DocumentSnapshot document = task.getResult();
                        if (document != null) {
                            String f = document.getString("First Name"+String.valueOf(removeP+1));
                            String l = document.getString("Last Name"+String.valueOf(removeP+1));
                            String e = document.getString("Email"+String.valueOf(removeP+1));
                            String p = document.getString("Phone Number"+String.valueOf(removeP+1));
                            reff = FirebaseDatabase.getInstance().getReference().child("signal");
                            reff.child("3").child("First Name").setValue(f);
                            reff.child("3").child("Last Name").setValue(l);
                            reff.child("3").child("Phone").setValue(p);
                            reff.child("3").child("E-Mail").setValue(e);
                        } else {
                            Log.d("LOGGER", "No such document");
                        }
                    } else {
                        Log.d("LOGGER", "get failed with ", task.getException());
                    }
                }
            });
            documentReference.update("First Name"+String.valueOf(removeP+1), FieldValue.delete());
            documentReference.update("Last Name"+String.valueOf(removeP+1), FieldValue.delete());
            documentReference.update("Email"+String.valueOf(removeP+1), FieldValue.delete());
            documentReference.update("Phone Number"+String.valueOf(removeP+1), FieldValue.delete());
            user.put("Number of Drivers",String.valueOf(removeP));
            documentReference.update(user);

            finish();
            startActivity(getIntent());
        } else {
            Toast.makeText(Drivers.this, "Cannot delete main driver", Toast.LENGTH_LONG).show();
        }
    }

    public void updateDriver(){
        startActivity(new Intent(getApplicationContext(), update.class));
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
        startActivity(new Intent(getApplicationContext(), Settings.class));
    }
}
