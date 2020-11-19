package com.example.capstone;

import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatDialogFragment;

public class addDriver extends AppCompatDialogFragment {
    private EditText fn, ln, ph, em;
    private addDriverListener listener;
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        LayoutInflater inflater = getActivity().getLayoutInflater();
        View view = inflater.inflate(R.layout.add_driver, null);

        builder.setView(view).setTitle("Add Driver").setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {

            }
        })
        .setPositiveButton("Add", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String fns = fn.getText().toString();
                String lns = ln.getText().toString();
                String phs = ph.getText().toString();
                String ems = fn.getText().toString();
                listener.applyTexts(fns, lns, phs, ems);
            }
        });

        fn = view.findViewById(R.id.fname);
        ln = view.findViewById(R.id.lname);
        ph = view.findViewById(R.id.phone);
        em = view.findViewById(R.id.email);

        return builder.create();
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);

        try {
            listener = (addDriverListener) context;
        } catch (ClassCastException e) {
            throw new ClassCastException(context.toString()+"must implement addDriverListener");
        }
    }

    public interface addDriverListener{
        void applyTexts(String fn, String ln, String ph, String em);
    }
}
