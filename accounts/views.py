import hashlib

from django.shortcuts import redirect, render
from django.db import connection, IntegrityError
from django.contrib import messages
from django.http import JsonResponse
# from django.contrib.auth.models import User

def signup(request):
    data = {
        'firstname': None,
        'lastname' : None,
        'username' : None,
        'email' : None,
        'phone' : None,
        'bankacc' : None,
        'creditcard' : None,
    }

    if request.method == 'GET':
        return render(request, "accounts/signup.html", data)

    elif request.method == 'POST':
        data.update({
            'firstname': request.POST['firstname'],
            'lastname': request.POST['lastname'],
            'username': request.POST['username'],
            'email': request.POST['email'],
            'phone': request.POST['phonenumber'],
            'bankacc': request.POST['bankaccount'],
            'creditcard': request.POST['creditcard'],
        })
        
        password1 = request.POST['password']
        password2 = request.POST['confirmpassword']

        if password1 != password2:
            messages.error(request, "Passwords did not match")
            return render(request, "accounts/signup.html", data)

        cursor = connection.cursor()
        query = "SELECT USERNAME FROM USERS WHERE USERNAME=%s"
        cursor.execute(query, [data['username']])
        result = cursor.fetchone()
        cursor.close()

        if result is not None:
            messages.error(request, 'Username already exists')
            data.update({'username' : None})
            #return redirect('signup', data)
            print(data)
            return render(request, "accounts/signup.html", data)
        else:
            try:
                hashed_password = hashlib.sha256(password1.encode()).hexdigest()
                cursor = connection.cursor()
                query = "INSERT INTO USERS(USERNAME, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, PASSWORD, BANK_ACC_NO, CREDIT_CARD_NO) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query,
                               [data['username'], data['firstname'], data['lastname'], data['email'], 
                               data['phone'], hashed_password, data['bankacc'], data['creditcard']])
                cursor.close()
            except IntegrityError:
                messages.error(request, 'This email already has an account')
                data.update({'email' : None})
                return render(request, "accounts/signup.html", data)

            """ user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password1)
            user.save()
            auth.login(request, user) """
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
        cursor.execute(query, [username, hashed_password])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            messages.error(request,"Invalid login credentials!")
            return redirect('signin')
        else:
            """ user = auth.authenticate(username=username, password=password)
            auth.login(request, user) """
            request.session['username'] = username
            return render(request, "pages/home.html")

def profile(request):
    if(request.session.has_key('username')):
        cursor = connection.cursor()
        query = "SELECT * FROM USERS WHERE USERNAME=%s"
        cursor.execute(query, [request.session['username']])
        result = cursor.fetchone()
        cursor.close()
        
        data = {
            'username': result[1],
            'firstname': result[2],
            'lastname': result[3],
            'email': result[4],
            'phone': result[5],
            'bankacc': result[8],
            'creditcard': result[9],
            'update':'disabled'
        }

        return render(request, 'accounts/profile.html', data)
    else:
        messages.error(request, "Session Expired")
        return render(request, 'accounts/signin.html')

def logout(request):
    request.session.flush()
    return redirect('home')


def addhome(request):
    cursor = connection.cursor()
    query = "SELECT * FROM COUNTRIES"
    cursor.execute(query)
    result1 = cursor.fetchall()
    result1 = [country[0] for country in result1]
    """ query= "Select STATE_NAME from STATES"
    cursor.execute(query)
    result2 = cursor.fetchall()
    result2 = [state[0] for state in result2]
    query = "Select CITY_NAME from CITIES"
    cursor.execute(query)
    result3 = cursor.fetchall()
    result3 = [state[0] for state in result3] """
    cursor.close()
    data = {
        'countries': result1,
        #'states': result2,
        #'cities': result3
    }
    return render(request, 'accounts/addhome.html', data)

def fetch_statenames(request, key):
    cursor = connection.cursor()
    query = "select STATE_NAME from STATES where COUNTRY_NAME=%s"
    cursor.execute(query,[key])
    result = cursor.fetchall()
    result = [state[0] for state in result]
    #print(JsonResponse(result,safe=False))
    cursor.close()
    return JsonResponse(result, safe=False)

def fetch_citynames(request, key1,key2):
    cursor = connection.cursor()
    query = "SELECT STATE_ID FROM STATES WHERE STATE_NAME=%s AND COUNTRY_NAME=%s "
    cursor.execute(query,[key2, key1])
    state_id = cursor.fetchone()
    query = "SELECT CITY_NAME FROM CITIES WHERE STATE_ID=%s"
    cursor.execute(query,[str(state_id[0])])
    result = cursor.fetchall()
    result = [city[0] for city in result]
    #print(JsonResponse(result,safe=False))
    cursor.close()
    print(result)
    return JsonResponse(result, safe=False)