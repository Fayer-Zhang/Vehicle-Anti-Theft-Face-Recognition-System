package com.example.capstone;

public class User {

    private String Firstname;
    private String Lastname;
    private String phone;
    private String email;

    public User(String fn, String ln, String ph, String em) {
        Firstname = fn;
        Lastname = ln;
        phone = ph;
        email = em;

    }

    public String getFirstname() {
        return Firstname;
    }

    public void setFirstname(String firstname) {
        Firstname = firstname;
    }

    public String getLastname() {
        return Lastname;
    }

    public void setLastname(String lastname) {
        Lastname = lastname;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

}
