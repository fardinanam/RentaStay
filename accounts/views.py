from asyncio.windows_events import NULL
import hashlib
from django.shortcuts import redirect, render
from django.db import connection, IntegrityError
from django.contrib import messages
from django.http import JsonResponse
from rentastay import definitions
from django.core.files.storage import FileSystemStorage
from rentastay.settings import MEDIA_ROOT
from datetime import datetime

hfeatures = ['Kitchen', 'Free Parking', 'Backyard', 'WiFi', 'Dryer', 'Washer', 'Pets Allowed', 'Balcony', 'Refrigerator', 
            'Security Cameras', 'Fire extinguisher', 'First Aid Kit', 'Microwave', '24/7 Electricity']

rfeatures = ['EV Charger', 'Extra Pillow and Blanket', 'Portable Fans', 'TV', 'Air Conditioner (AC)', 'Heater', 'Separate Bathroom', 'Common Bathroom',
            'Lockbox','Almirah']

selected_features = []

def is_username_unique(username):
    cursor = connection.cursor()
    query = """SELECT USERNAME 
            FROM USERS WHERE USERNAME=%s"""
    cursor.execute(query, [username])
    result = cursor.fetchone()
    print(result)
    cursor.close()

    if result is not None:
        return False
    
    return True

def IsHouseInputsValid(request,countryname,statename,cityname,streetname,postalcode,housename,housenumber,description):
    if countryname=="Country Name":
        messages.error(request,'Please select a country!!')
        return False
    elif statename=="State Name":
        messages.error(request,'Please select a state!!')
        return False
    elif cityname=="City name":
        messages.error(request,'Please select a city!!')
        return False
    elif streetname=="" or postalcode=="" or housename=="" or housenumber=="":
        messages.error(request,'Please fill up all the field!!')
        return False
    elif not request.FILES.get('upload1',False):
        messages.error(request, 'Please upload an image file of your house!!')
        return False
    return True

def IsRoomInputsValid(request,roomno,capacity,price):
    if roomno=="" or roomno==NULL:
        messages.error(request,'Please add a room number!!')
        return False
    elif capacity=="Capacity":
        messages.error(request,'Please select maximum capacity of the room!!')
        return False
    elif price=="" or price==NULL:
        messages.error(request,'Please input the room price!!')
        return False
    elif not request.FILES.get('uploadroom1',False):
        messages.error(request, 'Please upload an image file of the room!!')
        return False
    return True

def IsSignUpInputsValid(request, firstname, lastname, phonenumber, email, username):
    if username==NULL or username=="":
        messages.error(request,'Please input your username!!')
        return False
    elif email==NULL or email=="":
        messages.error(request,'Please input your email!!')
        return False
    elif firstname==NULL or firstname=="":
        messages.error(request,'Please input your first name!!')
        return False
    elif lastname==NULL or lastname=="":
        messages.error(request,'Please input your last name!!')
        return False
    elif phonenumber==NULL or phonenumber=="":
        messages.error(request,'Please five your phone number!!')
        return False

def IsProfileInputsValid(request, firstname, lastname, phonenumber):
    if firstname==NULL or firstname=="":
        messages.error(request,'Please input your first name!!')
        return False
    elif lastname==NULL or lastname=="":
        messages.error(request,'Please input your last name!!')
        return False
    elif phonenumber==NULL or phonenumber=="":
        messages.error(request,'Please five your phone number!!')
        return False
    return True

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
        firstname = request.POST.get('firstname'),
        lastname = request.POST.get('lastname'),
        username = request.POST.get('username'),
        email = request.POST.get('email'),
        phone = request.POST.get('phonenumber'),
        data.update({
            'firstname': firstname[0],
            'lastname': lastname[0],
            'username': username[0],
            'email': email[0],
            'phone': phone[0],
            'bankacc': request.POST.get('bankaccount'),
            'creditcard': request.POST.get('creditcard'),
        })
        
        if IsSignUpInputsValid(request, firstname, lastname, phone, email, username) == False:
            return render(request, "accounts/signup.html", data)
        
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirmpassword')

        if password1 != password2:
            messages.error(request, "Passwords did not match")
            return render(request, "accounts/signup.html", data)
        
        print("Username hoilo")
        print(data['username'])

        if is_username_unique(data['username'])== False:
            messages.error(request, 'Username already exists')
            data.update({'username' : None})
            return render(request, "accounts/signup.html", data)
        else:
            dateFormat = '%d-%b-%Y'
            joiningDate= datetime.strftime(datetime.now(), dateFormat)
            data.update({'joindate': joiningDate})
            try:
                hashed_password = hashlib.sha256(password1.encode()).hexdigest()
                cursor = connection.cursor()
                query = """INSERT INTO USERS(USERNAME, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, PASSWORD, BANK_ACC_NO, CREDIT_CARD_NO, JOIN_DATE) 
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, TO_DATE(%s, \'DD-Mon-YYYY\'))"""
                cursor.execute( query,
                                [data['username'], data['firstname'], data['lastname'], data['email'], 
                                data['phone'], hashed_password, data['bankacc'], data['creditcard'], data['joindate']])
                request.session['username'] = data['username']
                cursor.close()
            except IntegrityError:
                messages.error(request, 'This email already has an account')
                data.update({'email' : None})
                return render(request, "accounts/signup.html", data)

            if request.GET.get('next') is None:
                return redirect('home')
            else:
                return redirect(request.GET['next'])

def signin(request):
    if request.method == 'GET':
        return render(request, "accounts/signin.html")
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor = connection.cursor()
        query = """SELECT USERNAME, PROFILE_PIC, IS_HOST
                FROM USERS 
                WHERE USERNAME=%s AND PASSWORD=%s"""
        cursor.execute(query, [username, hashed_password])
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            messages.error(request,"Invalid login credentials!")
            return render(request, 'accounts/signin.html')
        else:
            request.session['username'] = username
            request.session['profile_pic'] = result[1]
            request.session['is_host'] = result[2]
            
            if request.GET.get('next') is None:
                return redirect('home')
            else:
                return redirect(request.GET.get('next'))

def profile(request):
    data = {
        'username': '',
        'firstname': '',
        'lastname': '',
        'email': '',
        'phone': '',
        'bankacc': '',
        'creditcard': ''
    }

    if(request.session.has_key('username')):
        cursor = connection.cursor()
        query = """SELECT *
                    FROM USERS
                    WHERE USERNAME=%s"""

        cursor.execute(query, [request.session['username']])
        result = definitions.dictfetchone(cursor)
        user_id = result['USER_ID']
        cursor.close()

        data.update({
            'username': result['USERNAME'],
            'firstname': result['FIRST_NAME'],
            'lastname': result['LAST_NAME'],
            'email': result['EMAIL'],
            'phone': result['PHONE_NO'],
            'bankacc': result['BANK_ACC_NO'],
            'creditcard': result['CREDIT_CARD_NO'],
            'profile_pic': result['PROFILE_PIC']
        })

        if request.method == 'GET':
            return render(request, 'accounts/profile.html', data)
        elif request.method == 'POST':
            data.update({
                'firstname': request.POST.get('firstname'),
                'lastname': request.POST.get('lastname'),
                'phone': request.POST.get('phonenumber'),
                'bankacc': request.POST.get('bankaccount'),
                'creditcard': request.POST.get('creditcard')
            })

            if data['username'] != request.POST.get('username') and is_username_unique(request.POST.get('username')) is False:
                messages.error(
                    request, 'Can not change to new username because the new username already exists')
                return render(request, "accounts/profile.html", data)
            elif data['username'] != request.POST.get('username'):
                cursor = connection.cursor()
                query = """UPDATE USERS
                        SET USERNAME = %s
                        WHERE USERNAME = %s"""
                cursor.execute(
                    query, [request.POST.get('username'), data['username']])
                
                
                messages.success(request, "Username updated!")
                data.update({
                    'username': request.POST.get('username')
                })
                request.session.update({
                    'username': data['username']
                })

            cursor = connection.cursor()
            query = """UPDATE USERS
                    SET FIRST_NAME = %s, 
                    LAST_NAME = %s,
                    PHONE_NO = %s,
                    BANK_ACC_NO = %s,
                    CREDIT_CARD_NO = %s
                    WHERE USERNAME = %s"""
            cursor.execute(query, [data['firstname'], data['lastname'], 
                data['phone'], data['bankacc'], data['creditcard'], data['username']])
            
            if request.FILES.get('profilePic',False):
                folder = MEDIA_ROOT + '/Users/' + str(request.session['username'])
                upload1 = request.FILES['profilePic']
                fss = FileSystemStorage(location=folder)
                file = fss.save(upload1.name, upload1)
                photoPath = '/media/Users/' + str(request.session['username']) + '/'+upload1.name
                file_url = fss.url(file)

                query = """UPDATE USERS SET PROFILE_PIC=%s WHERE USER_ID=%s"""
                request.session.update({
                    'profile_pic': photoPath
                })
                cursor.execute(query, [photoPath, str(user_id)])

                data.update({
                    'profile_pic': photoPath
                })
            
            query = """SELECT EMAIL 
                    FROM USERS
                    WHERE USERNAME = %s"""
            cursor.execute(query, [data['username']])
            result = cursor.fetchone()
            data.update({
                'email': result[0]
            })
            cursor.close()
            
            return render(request, 'accounts/profile.html', data)
    else:
        messages.error(request, "Session Expired")
        return redirect('signin')

def deleteprofile(request):
    cursor = connection.cursor()
    if request.method=='POST' and request.POST.get('YES', False) and request.POST.get('YES',False)=='deluser':
        query="""DELETE FROM USERS WHERE USERNAME=%s"""
        cursor.execute(query,[request.session.get('username')])
        request.session.flush()
        return JsonResponse({'url': ''}) 

def logout(request):
    request.session.flush()
    return redirect('home')

def addhome(request):
    datas ={
        'countries': None,
        'streetname': None,
        'postalcode': None,
        'house_id': None,
        'housename': None,
        'house_address': None,
        'housenumber':  None,
        'description': None,
    }
    cursor = connection.cursor()
    query = "SELECT * FROM COUNTRIES"
    cursor.execute(query)
    result1 = cursor.fetchall()
    result1 = [country[0] for country in result1]
    result1.sort()
    cursor.close()
    datas.update({
        'countries': result1,
    })
    data = {
        'countries': result1,
    }
    
    if request.method=='GET':
        cursor = connection.cursor()
        query = """SELECT BANK_ACC_NO
                FROM USERS WHERE USERNAME = %s"""
        cursor.execute(query, [request.session.get('username')])
        result = cursor.fetchone()
        cursor.close()

        if result[0] is None:
            messages.error(request, "Please update your bank account to become a host")
            return redirect('/accounts/profile/')

        return render(request, 'accounts/addhome.html', data)
    
    if request.method=='POST':
        countryname = request.POST.get('countryname','Country Name')
        statename = request.POST.get('statename','State Name')
        cityname = request.POST.get('cityname','City Name')
        datas.update({
            'streetname': request.POST.get('streetname',""),
            'postalcode': request.POST.get('postalcode',""),
            'housename': request.POST.get('housename',""),
            'housenumber': request.POST.get('housenumber',""),
            'description': request.POST.get('description',""),
        })
        #print(countryname + " " + statename + " " + cityname + " " + streetname + " " + postalcode + " " + housename + " " + housenumber + " " + description + " " + request.session['username'])
        if IsHouseInputsValid(request,countryname,statename,cityname,datas['streetname'],datas['postalcode'],datas['housename'],datas['housenumber'],datas['description']) == False:
            return render(request,'accounts/addhome.html',datas)
        cursor = connection.cursor()
        query = """SELECT USER_ID 
                FROM USERS WHERE USERNAME=%s"""
        cursor.execute(query,[request.session['username']])
        user_id = definitions.dictfetchone(cursor)
        if not bool(user_id):
            messages.error(request, 'Please login to your account!!')
            cursor.close()
            return redirect('signin')
        user_id = user_id["USER_ID"]
        #print("User id: " + str(user_id))
        query = """SELECT STATE_ID 
                FROM STATES 
                WHERE STATE_NAME=%s AND COUNTRY_NAME=%s"""
        cursor.execute(query,[statename, countryname])
        state_id = definitions.dictfetchone(cursor)
        state_id = state_id["STATE_ID"]
        #print("State id: " + str(state_id))
        query = """SELECT CITY_ID 
                FROM CITIES 
                WHERE CITY_NAME=%s AND STATE_ID=%s"""
        cursor.execute(query,[cityname, str(state_id)])
        city_id = definitions.dictfetchone(cursor)
        city_id = city_id["CITY_ID"]
        #print("City id: " + str(city_id))
        query = """SELECT ADDRESS_ID 
                FROM ADDRESSES WHERE STREET=%s AND POST_CODE=%s AND CITY_ID=%s"""
        cursor.execute(
            query, [str(datas['streetname']), str(datas['postalcode']), str(city_id)])
        address_id = definitions.dictfetchone(cursor)
        if not bool(address_id):
            try:
                address_id = cursor.callfunc('INSERT_ADDRESS_RETURN_ADDRESS_ID', int,
                    [str(datas['streetname']), str(datas['postalcode']), str(city_id)])
            except IntegrityError:
                messages.error(request, "A house with this address already exists")
                return render(request, 'accounts/addhome.html', datas)
            
            if not bool(address_id):
                messages.error(request, 'Can\'t find the address!!')
                cursor.close()
                return render(request,'accounts/addhome.html',datas)
        if isinstance(address_id, int) is False:
            address_id = address_id["ADDRESS_ID"]

        house_id = cursor.callfunc('INSERT_HOUSE_RETURN_HOUSE_ID', int,
            [str(user_id), str(address_id), datas['housename'], datas['housenumber'], datas['description']])
        if not bool(house_id):
            messages.error(request, 'Can\'t find the house!!')
            cursor.close()
            return render(request,'accounts/addhome.html',datas)
        # house_id = house_id["HOUSE_ID"]
        datas.update({
            'house_id': str(house_id),
        })
        if request.FILES.get('upload1',False):
            folder = MEDIA_ROOT + '/Houses/' + str(house_id) + '/HousePic/'
            upload1 = request.FILES['upload1']
            fss = FileSystemStorage(location=folder)
            file = fss.save(upload1.name, upload1)
            photoPath = '/media/Houses/' + str(house_id) + '/HousePic/'+upload1.name
            file_url = fss.url(file)

            query = """INSERT INTO HOUSE_PHOTOS_PATH VALUES (%s, %s)"""
            cursor.execute(query, [str(house_id), photoPath])

        cursor.close()
        #return render(request,'accounts/home_preview.html',datas)
        return redirect('yourhouses')
        

def homepreview(request,house_id):
    cursor = connection.cursor()
    if request.method=='POST' and request.POST.get('YES', False) and request.POST.get('YES',False)=='delhouse':
        houseid=request.POST.get('house_id')
        query="""DELETE FROM HOUSES WHERE HOUSE_ID=%s"""
        cursor.execute(query,[str(houseid)])
        return JsonResponse({'url': '/yourhouses/'}) 
    query="""SELECT ADDRESS_ID, HOUSE_NAME, DESCRIPTION, HOUSE_NO, FEATURES
            FROM HOUSES
            WHERE HOUSE_ID=%s"""
    cursor.execute(query,[str(house_id)])
    result = definitions.dictfetchone(cursor)

    if not bool(result):
            messages.error(request, 'Can\'t find the house!!')
            cursor.close()
            return redirect('home')

    address_id = result["ADDRESS_ID"]
    housename = result["HOUSE_NAME"]
    description = result["DESCRIPTION"]
    house_no = result["HOUSE_NO"]
    housefeatures = result["FEATURES"]
    query="""select a.STREET,c.CITY_NAME,s.STATE_NAME,s.COUNTRY_NAME
            from ADDRESSES a 
            JOIN CITIES c 
            ON (a.CITY_ID=c.CITY_ID)
            join STATES s
            ON (c.STATE_ID=s.STATE_ID)
            WHERE a.ADDRESS_ID=%s"""
    cursor.execute(query,[str(address_id)])
    result = definitions.dictfetchone(cursor)

    if not bool(result):
        messages.error(request, 'Can\'t find the address of the house!!')
        cursor.close()
        return redirect('home')

    streetname = result["STREET"]
    cityname = result["CITY_NAME"]
    statename = result["STATE_NAME"]
    countryname = result["COUNTRY_NAME"]
    #print(streetname)
    query = """SELECT COUNT(*) FROM HOUSE_PHOTOS_PATH WHERE HOUSE_ID=%s"""
    cursor.execute(query,[str(house_id)])
    result = cursor.fetchone()
    if request.method=="POST":
        for i in range(result[0],6):
            #print('upload'+str(i))
            if request.FILES.get('upload'+str(i),False):
                folder = MEDIA_ROOT + '/Houses/' + str(house_id) + '/HousePic/'
                upload = request.FILES['upload'+str(i)]
                fss = FileSystemStorage(location=folder)
                file = fss.save(upload.name, upload)
                photoPath = '/media/Houses/' + str(house_id) + '/HousePic/'+upload.name
                file_url = fss.url(file)
                query = """INSERT INTO HOUSE_PHOTOS_PATH VALUES (%s, %s)"""
                cursor.execute(query, [str(house_id), photoPath])
                
    query="""SELECT PATH FROM HOUSE_PHOTOS_PATH WHERE HOUSE_ID=%s"""
    cursor.execute(query,[str(house_id)])
    result = cursor.fetchall()
    photos_path = [photo[0] for photo in result]
    #print(address_id,housename,description)
    #print(photos_path)
    query="""SELECT ROOM_NO FROM ROOMS 
            WHERE HOUSE_ID=%s
            ORDER BY ROOM_NO ASC"""
    cursor.execute(query,[str(house_id)])
    result = cursor.fetchall()
    rooms = [room[0] for room in result]
    
    if((housefeatures is None) or (housefeatures is NULL)):
        fhouse = None
    else:
        x = housefeatures.split("\\")
        del x[-1]
        fhouse = x
        
    minPrice = cursor.callfunc('GET_MIN_PRICE', float, [house_id])
    maxPrice = cursor.callfunc('GET_MAX_PRICE', float, [house_id])
    
    data ={
        'house_id': str(house_id),
        'housename': housename,
        'house_address': str(house_no) + ", " + str(streetname) + ", " +  str(cityname) + ", " + str(statename) + ", " + str(countryname),
        'description': description,
        'photos_url': photos_path,
        'rooms': rooms,
        'features' : fhouse,
        'minprice' : minPrice,
        'maxprice' : maxPrice,
    }
    cursor.close()
    return render(request, 'accounts/home_preview.html',data)

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
    #print(result)
    return JsonResponse(result, safe=False)

def fetch_no_of_house_pics(request, house_id):
    cursor = connection.cursor()
    query = "SELECT USER_ID FROM USERS WHERE USERNAME=%s"
    cursor.execute(query,[request.session['username']])
    user_id = definitions.dictfetchone(cursor)

    if not bool(user_id):
        messages.error(request, 'Please login to your account!!')
        cursor.close()
        return redirect('signin')

    user_id = user_id["USER_ID"]
    query = "SELECT PATH FROM HOUSE_PHOTOS_PATH WHERE HOUSE_ID=%s"
    cursor.execute(query,[str(house_id)])
    photos_paths = definitions.dictfetchall(cursor)

    result = [len(photos_paths)]
    cursor.close()
    return JsonResponse(result, safe=False)

def fetch_no_of_room_pics(request, house_id, roomnumber):
    cursor = connection.cursor()
    query = "SELECT USER_ID FROM USERS WHERE USERNAME=%s"
    cursor.execute(query,[request.session['username']])
    user_id = definitions.dictfetchone(cursor)

    if not bool(user_id):
        messages.error(request, 'Please login to your account!!')
        cursor.close()
        return redirect('signin')

    user_id = user_id["USER_ID"]
    query = "SELECT PATH FROM ROOM_PHOTOS_PATH WHERE HOUSE_ID=%s AND ROOM_NO=%s"
    cursor.execute(query,[str(house_id),str(roomnumber)])
    photos_paths = definitions.dictfetchall(cursor)
    
    result = [len(photos_paths)]
    cursor.close()
    return JsonResponse(result, safe=False)

def addroom(request,house_id):
    data ={
        'house_id': str(house_id),
        'housename': None,
        'roomnumber': None,
        'capacity': None,
        'roomprice': None,
        'description': None,
    }
    cursor = connection.cursor()
    query = "SELECT HOUSE_NAME FROM HOUSES WHERE HOUSE_ID=%s"
    cursor.execute(query,[str(house_id)])
    house_name = definitions.dictfetchone(cursor)

    if not bool(house_name):
        messages.error(request, 'Can\'t find the house!!')
        cursor.close()
        return redirect('home')

    house_name = house_name["HOUSE_NAME"]
    data.update({
        'housename': house_name,
    })
    
    data1 ={
        'house_id': str(house_id),
        'housename': house_name,
    }
    
    if request.method=='GET':
        return render(request,'accounts/addroom.html',data1)

    if request.method == 'POST':
        data.update({
            'roomnumber': request.POST['roomnumber'],
            'capacity': request.POST.get('maxcapacity','Capacity'),
            'roomprice': request.POST['roomprice'],
            'description': request.POST['description'],
        })
        if IsRoomInputsValid(request,data['roomnumber'],data['capacity'],data['roomprice'])==False:
            return render(request,'accounts/addroom.html',data)
            
        query = """INSERT INTO ROOMS(HOUSE_ID,ROOM_NO,MAX_CAPACITY,DESCRIPTION,PRICE,OFFER_PCT) 
                VALUES(%s,%s,%s,%s,%s,'0')"""
        cursor.execute(query,[str(house_id),str(data['roomnumber']),str(data['capacity']),data['description'],data['roomprice']])
        if request.FILES.get('uploadroom1',False):
            folder = MEDIA_ROOT + '/Houses/' + str(house_id) + '/Rooms/' + str(data['roomnumber']) + '/'
            upload = request.FILES['uploadroom1']
            fss = FileSystemStorage(location=folder)
            file = fss.save(upload.name, upload)
            photoPath = '/media/Houses/' + str(house_id) + '/Rooms/' + str(data['roomnumber']) + '/' + upload.name
            file_url = fss.url(file)
            query = """INSERT INTO ROOM_PHOTOS_PATH VALUES (%s, %s, %s)"""
            cursor.execute(query, [house_id, data['roomnumber'], photoPath])
        
        cursor.close()
        #return render(request,'accounts/room_preview.html',data)
        return redirect('homepreview',house_id=str(house_id))
        

def roompreview(request,house_id,roomnumber):
    cursor = connection.cursor()
    if request.method=='POST' and request.POST.get('YES', False) and request.POST.get('YES',False)=='delroom':
        houseid=request.POST.get('house_id')
        room = request.POST.get('roomnumber')
        query="""DELETE FROM ROOMS WHERE HOUSE_ID=%s AND ROOM_NO=%s"""
        cursor.execute(query,[str(houseid),str(room)])
        return JsonResponse({'url': '/accounts/homepreview/'+str(houseid)})
    query="""SELECT ADDRESS_ID, HOUSE_NAME, HOUSE_NO
            FROM HOUSES
            WHERE HOUSE_ID=%s"""
    cursor.execute(query,[str(house_id)])
    result = definitions.dictfetchone(cursor)

    if not bool(result):
            messages.error(request, 'Can\'t find the house!!')
            cursor.close()
            return redirect('home')

    address_id = result["ADDRESS_ID"]
    housename = result["HOUSE_NAME"]
    house_no = result["HOUSE_NO"]
    query="""select a.STREET,c.CITY_NAME,s.STATE_NAME,s.COUNTRY_NAME
            from ADDRESSES a 
            JOIN CITIES c 
            ON (a.CITY_ID=c.CITY_ID)
            join STATES s
            ON (c.STATE_ID=s.STATE_ID)
            WHERE a.ADDRESS_ID=%s"""
    cursor.execute(query,[str(address_id)])
    result = definitions.dictfetchone(cursor)

    if not bool(result):
        messages.error(request, 'Can\'t find the address of the house!!')
        cursor.close()
        return redirect('home')

    streetname = result["STREET"]
    cityname = result["CITY_NAME"]
    statename = result["STATE_NAME"]
    countryname = result["COUNTRY_NAME"]
    query = """SELECT COUNT(*) from ROOM_PHOTOS_PATH WHERE HOUSE_ID=%s AND ROOM_NO=%s"""
    cursor.execute(query,[str(house_id),str(roomnumber)])
    result = cursor.fetchone()
    if request.method=="POST":
        for i in range(result[0]+1,6):
            #print('upload'+str(i))
            if request.FILES.get('uploadroom'+str(i),False):
                folder = MEDIA_ROOT + '/Houses/' + str(house_id) + '/Rooms/' + str(roomnumber) + '/'
                upload = request.FILES['uploadroom'+str(i)]
                fss = FileSystemStorage(location=folder)
                file = fss.save(upload.name, upload)
                photoPath = '/media/Houses/' + str(house_id) + '/Rooms/' + str(roomnumber) + '/' + upload.name
                file_url = fss.url(file)
                query = """INSERT INTO ROOM_PHOTOS_PATH VALUES (%s, %s,%s)"""
                cursor.execute(query, [str(house_id),str(roomnumber),photoPath])
                
    query="""SELECT PATH FROM ROOM_PHOTOS_PATH WHERE HOUSE_ID=%s AND ROOM_NO=%s"""
    cursor.execute(query,[str(house_id),str(roomnumber)])
    result = cursor.fetchall()
    photos_path = [photo[0] for photo in result]
    
    query="""SELECT DESCRIPTION,MAX_CAPACITY,PRICE,OFFER_PCT,FEATURES FROM ROOMS WHERE HOUSE_ID=%s AND ROOM_NO=%s"""
    cursor.execute(query,[str(house_id),str(roomnumber)])
    result = definitions.dictfetchone(cursor)
    description = result['DESCRIPTION']
    capacity = result['MAX_CAPACITY']
    price = result['PRICE']
    offer_pct = result['OFFER_PCT']
    roomfeatures = result['FEATURES']
    
    if((roomfeatures is None) or (roomfeatures is NULL)):
        froom = None
    else:
        x = roomfeatures.split("\\")
        del x[-1]
        froom = x
    
    data ={
        'house_id': str(house_id),
        'housename': housename,
        'roomnumber': roomnumber,
        'house_address': str(house_no) + ", " +  str(streetname) + ", " +  str(cityname) + ", " + str(statename) + ", " + str(countryname),
        'description': description,
        'photos_url': photos_path,
        'capacity': capacity,
        'price': price,
        'offer_pct': offer_pct,
        'features' : froom,
    }
    cursor.close()
    return render(request, 'accounts/room_preview.html',data)

def edithouseinfo(request,house_id):
    cursor = connection.cursor()
    if request.method=="POST":
        if request.POST.get('deletedImg',False):
            path = request.POST.get('deletedImg',False)
            query="""DELETE FROM HOUSE_PHOTOS_PATH WHERE HOUSE_ID=%s AND PATH=%s"""
            cursor.execute(query,[str(house_id),str(path)]) 
        
        elif request.POST.get('description',False):
            description = request.POST['description']
            housename = request.POST['housename']
            query="""UPDATE HOUSES SET HOUSE_NAME=%s, 
                    DESCRIPTION=%s 
                    WHERE HOUSE_ID=%s"""
            cursor.execute(query,[str(housename), str(description) , str(house_id)])
        else:
            selected_features.clear()
            text = ""
            for feature in hfeatures:
                if request.POST.get(feature, False):
                    selected_features.append(feature)
                    text+=(feature+"\\")
            if(len(selected_features)!=0):
                query="""UPDATE HOUSES SET FEATURES=%s WHERE HOUSE_ID=%s"""
                cursor.execute(query,[str(text), str(house_id)])

    query="""SELECT ADDRESS_ID, HOUSE_NAME, DESCRIPTION, HOUSE_NO, FEATURES
            FROM HOUSES
            WHERE HOUSE_ID=%s"""
    cursor.execute(query,[str(house_id)])
    result = definitions.dictfetchone(cursor)

    if not bool(result):
            messages.error(request, 'Can\'t find the house!!')
            cursor.close()
            return redirect('home')

    address_id = result["ADDRESS_ID"]
    housename = result["HOUSE_NAME"]
    description = result["DESCRIPTION"]
    house_no = result["HOUSE_NO"]
    housefeatures = result["FEATURES"]
    query="""select a.STREET,c.CITY_NAME,s.STATE_NAME,s.COUNTRY_NAME
            from ADDRESSES a 
            JOIN CITIES c 
            ON (a.CITY_ID=c.CITY_ID)
            join STATES s
            ON (c.STATE_ID=s.STATE_ID)
            WHERE a.ADDRESS_ID=%s"""
    cursor.execute(query,[str(address_id)])
    result = definitions.dictfetchone(cursor)

    if not bool(result):
        messages.error(request, 'Can\'t find the address of the house!!')
        cursor.close()
        return redirect('home')

    streetname = result["STREET"]
    cityname = result["CITY_NAME"]
    statename = result["STATE_NAME"]
    countryname = result["COUNTRY_NAME"]
    
    query="""SELECT PATH FROM HOUSE_PHOTOS_PATH WHERE HOUSE_ID=%s"""
    cursor.execute(query,[str(house_id)])
    result = cursor.fetchall()
    photos_path = [photo[0] for photo in result]
    if((housefeatures is None) or (housefeatures is NULL)):
        fhouse = None
    else:
        x = housefeatures.split("\\")
        del x[-1]
        fhouse = x
    
    data ={
        'house_id': str(house_id),
        'housename': housename,
        'house_address': str(house_no) + ", " +  str(streetname) + ", " +  str(cityname) + ", " + str(statename) + ", " + str(countryname),
        'description': description,
        'photos_url': photos_path,
        'features' : hfeatures,
        'sfeatures': fhouse,
    }
    cursor.close()
    return render(request,'accounts/edithome.html',data)


def editroominfo(request,house_id, roomnumber):
    cursor = connection.cursor()
    if request.method=="POST":
        if request.POST.get('deletedImg',False):
            path = request.POST.get('deletedImg',False)
            query="""DELETE FROM ROOM_PHOTOS_PATH WHERE HOUSE_ID=%s AND ROOM_NO=%s AND PATH=%s"""
            cursor.execute(query,[str(house_id), str(roomnumber), str(path)]) 
        
        elif request.POST.get('description',False):
            description = request.POST['description']
            price = request.POST['roomprice']
            maxcap = request.POST.get('maxcapacity','Capacity')
            offer = request.POST['offer_pct']
            query="""UPDATE ROOMS SET 
                    DESCRIPTION=%s, 
                    PRICE=%s,
                    OFFER_PCT=%s
                    WHERE ROOM_NO=%s AND HOUSE_ID=%s"""
            cursor.execute(query,[description, str(price), str(offer), str(roomnumber) , str(house_id)])
            if maxcap!='Capacity':
                query="""UPDATE ROOMS SET 
                        MAX_CAPACITY=%s
                        WHERE ROOM_NO=%s AND HOUSE_ID=%s"""
                cursor.execute(query,[str(maxcap), str(roomnumber) , str(house_id)])
                
        else:
            selected_features.clear()
            text = ""
            for feature in rfeatures:
                if request.POST.get(feature, False):
                    selected_features.append(feature)
                    text+=(feature+"\\")
            if(len(selected_features)!=0):
                query="""UPDATE ROOMS SET FEATURES=%s WHERE ROOM_NO=%s AND HOUSE_ID=%s"""
                cursor.execute(query,[str(text), str(roomnumber), str(house_id)])

    query="""SELECT ADDRESS_ID, HOUSE_NAME, HOUSE_NO
            FROM HOUSES
            WHERE HOUSE_ID=%s"""
    cursor.execute(query,[str(house_id)])
    result = definitions.dictfetchone(cursor)

    if not bool(result):
            messages.error(request, 'Can\'t find the house!!')
            cursor.close()
            return redirect('home')

    address_id = result["ADDRESS_ID"]
    housename = result["HOUSE_NAME"]
    house_no = result["HOUSE_NO"]
    query="""select a.STREET,c.CITY_NAME,s.STATE_NAME,s.COUNTRY_NAME
            from ADDRESSES a 
            JOIN CITIES c 
            ON (a.CITY_ID=c.CITY_ID)
            join STATES s
            ON (c.STATE_ID=s.STATE_ID)
            WHERE a.ADDRESS_ID=%s"""
    cursor.execute(query,[str(address_id)])
    result = definitions.dictfetchone(cursor)

    if not bool(result):
        messages.error(request, 'Can\'t find the address of the house!!')
        cursor.close()
        return redirect('home')

    streetname = result["STREET"]
    cityname = result["CITY_NAME"]
    statename = result["STATE_NAME"]
    countryname = result["COUNTRY_NAME"]
    
    query="""SELECT PATH FROM ROOM_PHOTOS_PATH WHERE HOUSE_ID=%s AND ROOM_NO=%s"""
    cursor.execute(query,[str(house_id),str(roomnumber)])
    result = cursor.fetchall()
    photos_path = [photo[0] for photo in result]
        
    query="""SELECT DESCRIPTION,MAX_CAPACITY,PRICE,OFFER_PCT,FEATURES FROM ROOMS WHERE HOUSE_ID=%s AND ROOM_NO=%s"""
    cursor.execute(query,[str(house_id),str(roomnumber)])
    result = definitions.dictfetchone(cursor)
    description = result['DESCRIPTION']
    capacity = result['MAX_CAPACITY']
    price = result['PRICE']
    offer_pct = result['OFFER_PCT']
    roomfeatures = result['FEATURES']
    
    if((roomfeatures is None) or (roomfeatures is NULL)):
        froom = None
    else:
        x = roomfeatures.split("\\")
        del x[-1]
        froom = x
    
    data ={
        'house_id': str(house_id),
        'housename': housename,
        'roomnumber': roomnumber,
        'house_address': str(house_no) + ", " +  str(streetname) + ", " +  str(cityname) + ", " + str(statename) + ", " + str(countryname),
        'description': description,
        'photos_url': photos_path,
        'capacity': str(capacity),
        'price': price,
        'offer_pct': offer_pct,
        'features' : rfeatures,
        'sfeatures': froom,
    }
    cursor.close()
    return render(request,'accounts/editroom.html',data)