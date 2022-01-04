import hashlib

from django.shortcuts import redirect, render
from django.db import connection, IntegrityError
from django.contrib import messages

def signup(request):
    if request.method == 'GET':
        return render(request, "accounts/signup.html")
    elif request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phonenumber']
        password1 = request.POST['password']
        password2 = request.POST['confirmpassword']
        bankacc = request.POST['bankaccount']
        creditcard = request.POST['creditcard']

        if(password1 != password2):
            messages.error(request, "Password did not match")
            return redirect('signup')
        
        cursor = connection.cursor()
        query = "SELECT USERNAME FROM USERS WHERE USERNAME=%s"
        cursor.execute(query, [username])
        result = cursor.fetchone()
        cursor.close()

        if result != None:
            messages.error(request, 'Username already exists')
            return redirect('signup')
        else:
            try:
                hashed_password = hashlib.sha256(password1.encode()).hexdigest()
                cursor = connection.cursor()
                query = "INSERT INTO USERS(USERNAME, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, PASSWORD, BANK_ACC_NO, CREDIT_CARD_NO) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, [username, firstname, lastname, email, phone, hashed_password, bankacc, creditcard])
                cursor.close()
            except IntegrityError:
                messages.error(request, 'This email already has an account')
                return redirect('signup')

            # TODO: redirect to home
            return render(request, "accounts/signup.html")
        


