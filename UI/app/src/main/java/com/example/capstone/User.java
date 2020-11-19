package com.example.capstone;

public class User {

    private String Firstname;
    private String Lastname;
    private Long phone;
    private String email;
    private String password;

    public User(String fn, String ln, Long ph, String em, String pw) {
        Firstname = fn;
        Lastname = ln;
        phone = ph;
        email = em;
        password = pw;
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

    public Long getPhone() {
        return phone;
    }

    public void setPhone(Long phone) {
        this.phone = phone;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
