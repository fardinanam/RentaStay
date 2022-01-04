function validateSignupForm() {
    console.log("okay");
    let password1 = document.getElementById('password').value;
    let password2 = document.getElementById('confirmpassword').value;

    if(password1.locateCompare(password2) != 0) {
        alert("Passwords did not match");
        return false;
    } else {
        return true;
    }
}