package com.example.capstone;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.DownloadManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.view.View;
import android.widget.ImageView;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.storage.FileDownloadTask;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

public class VThiefPictures extends AppCompatActivity {
    FirebaseAuth fAuth;
    private ImageView mImageView;
    private FirebaseStorage storage=FirebaseStorage.getInstance();
    ImageView img1, img2, img3;
    DatabaseReference reff;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_vthief_pictures);
        fAuth = FirebaseAuth.getInstance();

        img1 = findViewById(R.id.image1);
        img2 = findViewById(R.id.image2);
        img3 = findViewById(R.id.image3);

        try {
            StorageReference storageReference1 = storage.getReferenceFromUrl( "gs://vehicleantitheftrecognition.appspot.com/Photos_of_Thieves/Thief_1/0.jpg");
            StorageReference storageReference2 = storage.getReferenceFromUrl( "gs://vehicleantitheftrecognition.appspot.com/Photos_of_Thieves/Thief_2/0.jpg");
            StorageReference storageReference3 = storage.getReferenceFromUrl( "gs://vehicleantitheftrecognition.appspot.com/Photos_of_Thieves/Thief_3/0.jpg");
            final File file1 = File.createTempFile("image1", "jpg");
            final File file2 = File.createTempFile("image2", "jpg");
            final File file3 = File.createTempFile("image3", "jpg");
            storageReference1.getFile(file1).addOnSuccessListener(new OnSuccessListener<FileDownloadTask.TaskSnapshot>() {
                @Override
                public void onSuccess(FileDownloadTask.TaskSnapshot taskSnapshot) {
                    Bitmap bitmap=BitmapFactory.decodeFile(file1.getAbsolutePath());
                    img1.setImageBitmap(bitmap);
                }
            });
            storageReference2.getFile(file2).addOnSuccessListener(new OnSuccessListener<FileDownloadTask.TaskSnapshot>() {
                @Override
                public void onSuccess(FileDownloadTask.TaskSnapshot taskSnapshot) {
                    Bitmap bitmap=BitmapFactory.decodeFile(file2.getAbsolutePath());
                    img2.setImageBitmap(bitmap);
                }
            });
            storageReference3.getFile(file3).addOnSuccessListener(new OnSuccessListener<FileDownloadTask.TaskSnapshot>() {
                @Override
                public void onSuccess(FileDownloadTask.TaskSnapshot taskSnapshot) {
                    Bitmap bitmap=BitmapFactory.decodeFile(file3.getAbsolutePath());
                    img3.setImageBitmap(bitmap);
                }
            });
        } catch (IOException e){
            e.printStackTrace();
        }

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
