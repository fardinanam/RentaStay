import hashlib

from django.shortcuts import redirect, render
from django.db import connection, IntegrityError
from django.contrib import messages, auth
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'GET':
        data = {
            'firstname': None,
            'lastname' : None,
            'username' : None,
            'email' : None,
            'phone' : None,
            'bankacc' : None,
            'creditcard' : None,
        }
        print(data)
        return render(request, "accounts/signup.html", data)
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

        if password1 != password2:
            messages.error(request, "Password did not match")
            data = {
                'firstname': firstname,
                'lastname' : lastname,
                'username' : username,
                'email' : email,
                'phone' : phone,
                'bankacc' : bankacc,
                'creditcard' : creditcard,
            }
            #return redirect('signup', data)
            print(data)
            return render(request, "accounts/signup.html", data)

        cursor = connection.cursor()
        query = "SELECT USERNAME FROM USERS WHERE USERNAME=%s"
        cursor.execute(query, [username])
        result = cursor.fetchone()
        cursor.close()

        if result is not None:
            messages.error(request, 'Username already exists')
            data = {
                'firstname': firstname,
                'lastname' : lastname,
                'username' : None,
                'email' : email,
                'phone' : phone,
                'bankacc' : bankacc,
                'creditcard' : creditcard,
            }
            #return redirect('signup', data)
            print(data)
            return render(request, "accounts/signup.html", data)
        else:
            try:
                hashed_password = hashlib.sha256(password1.encode()).hexdigest()
                cursor = connection.cursor()
                query = "INSERT INTO USERS(USERNAME, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, PASSWORD, BANK_ACC_NO, CREDIT_CARD_NO) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query,
                               [username, firstname, lastname, email, phone, hashed_password, bankacc, creditcard])
                cursor.close()
            except IntegrityError:
                messages.error(request, 'This email already has an account')
                data = {
                    'firstname': firstname,
                    'lastname' : lastname,
                    'username' : username,
                    'email' : None,
                    'phone' : phone,
                    'bankacc' : bankacc,
                    'creditcard' : creditcard,
                }
                #return redirect('signup', data)
                print(data)
                return render(request, "accounts/signup.html", data)

            user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password1)
            user.save()
            auth.login(request, user)
            # TODO: redirect to home
            return render(request, "pages/home.html")
        
        
def signin(request):
    if request.method == 'GET':
        return render(request, "accounts/signin.html")
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor = connection.cursor()
        query = "SELECT USERNAME FROM USERS WHERE USERNAME=%s AND PASSWORD=%s"
        cursor.execute(query, [username,hashed_password])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            messages.error(request,"Invalid login credentials!!")
            return redirect('signin')
        else:
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return render(request, "pages/home.html")
        
        
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')
