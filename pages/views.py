from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from rentastay import definitions
from django.http import JsonResponse
from django.contrib import messages

from datetime import datetime

def getHouses():
    cursor = connection.cursor()
    query = """SELECT HOUSE_ID, HOUSE_NAME, CITY_NAME, STATE_NAME, COUNTRY_NAME
            FROM HOUSES JOIN ADDRESSES USING(ADDRESS_ID) 
            JOIN CITIES USING(CITY_ID) 
            JOIN STATES USING(STATE_ID) 
            JOIN COUNTRIES USING(COUNTRY_NAME)"""
    cursor.execute(query)
    #print(cursor.fetchone())
    result = definitions.dictfetchall(cursor)
    #print(result)
    cursor.close()

    return result

def getYourHouses(request):
    cursor = connection.cursor()
    query = "SELECT USER_ID FROM USERS WHERE USERNAME=%s"
    cursor.execute(query,[request.session['username']])
    user_id = definitions.dictfetchone(cursor)
    if not bool(user_id):
        messages.error(request, 'Please login to your account!!')
        cursor.close()
        return redirect('signin')
    user_id = user_id["USER_ID"]
    query = "SELECT HOUSE_ID FROM HOUSES WHERE USER_ID=%s"
    cursor.execute(query,[str(user_id)])
    result1 = cursor.fetchall()
    result1 = [house_id[0] for house_id in result1]
    fetchedData = []
    for i in result1:
        query = """SELECT HOUSE_ID, HOUSE_NAME, CITY_NAME, STATE_NAME, COUNTRY_NAME
            FROM HOUSES JOIN ADDRESSES USING(ADDRESS_ID) 
            JOIN CITIES USING(CITY_ID) 
            JOIN STATES USING(STATE_ID) 
            JOIN COUNTRIES USING(COUNTRY_NAME)
            WHERE HOUSE_ID=%s"""
        cursor.execute(query,[str(i)])
        fetchedData.append(cursor.fetchone())
        columns = [col[0] for col in cursor.description]
        
    cursor.close()
    if len(fetchedData)==0:
        newlst=None
    else:
        newlst = [
            dict(zip(columns, row))
            for row in fetchedData
        ]
    return newlst

def home(request):
    houses = getHouses()
    data = {'houses':houses}
    # print(houses)
    return render(request, 'pages/home.html', data)

def yourhouses(request):
    houses = getYourHouses(request)
    data = {'houses':houses}
    # print(houses)
    return render(request,'pages/yourhouses.html',data)

def getJsonHouseData(request):
    houses = getHouses()
    return JsonResponse({'data':houses})

def getJsonYourHouseData(request):
    houses = getYourHouses(request)
    return JsonResponse({'data':houses})

def getJsonHousePhotosPath(request, house_id):
    cursor = connection.cursor()
    query = """SELECT PATH
            FROM HOUSE_PHOTOS_PATH
            WHERE HOUSE_ID = %s;"""
    cursor.execute(query, [house_id])
    result = definitions.dictfetchall(cursor)
    
    return JsonResponse({'paths':result})

def getJsonHousePriceRange(request, house_id):
    cursor = connection.cursor()
    minPrice = cursor.callfunc('GET_MIN_PRICE', float, [house_id])
    maxPrice = cursor.callfunc('GET_MAX_PRICE', float, [house_id])

    return JsonResponse({'minPrice':minPrice, 'maxPrice':maxPrice})

# def getJsonAvailableRoomsData(request, house_id, checkIn, checkOut, guests):
#     cursor = connection.cursor()
#     query = """SELECT *
#             FROM ROOMS
#             WHERE HOUSE_ID = %s"""
#     cursor.execute(query, [house_id])
#     rooms = definitions.dictfetchall(cursor)
#     rooms = sorted(rooms, key=lambda i: i['ROOM_NO'])


def house(request, house_id):
    # print(f"house id from GET is {houseId}")
    cursor = connection.cursor()
    query = """SELECT * 
            FROM HOUSES JOIN USERS USING(USER_ID)
            JOIN ADDRESSES USING (ADDRESS_ID)
            JOIN CITIES USING (CITY_ID)
            JOIN STATES USING (STATE_ID)
            JOIN COUNTRIES USING(COUNTRY_NAME)
            WHERE HOUSE_ID = %s"""
    cursor.execute(query, [house_id])
    result = definitions.dictfetchone(cursor)

    minPrice = cursor.callfunc('GET_MIN_PRICE', float, [house_id])
    maxPrice = cursor.callfunc('GET_MAX_PRICE', float, [house_id])

    result.update({
        'MIN_PRICE': minPrice,
        'MAX_PRICE': maxPrice
    })

    # query = """SELECT * 
    #         FROM ROOMS
    #         WHERE HOUSE_ID = %s"""
    # cursor.execute(query, [house_id])
    # rooms = definitions.dictfetchall(cursor)
    # rooms = sorted(rooms, key=lambda i: i['ROOM_NO'])

    query = """SELECT PATH
            FROM HOUSE_PHOTOS_PATH
            WHERE HOUSE_ID = %s"""
    cursor.execute(query, [house_id])
    photosPath = definitions.dictfetchall(cursor)
    cursor.close()

    return render(request, 'pages/house.html', {'house':result, 'photos_url': photosPath})

def reservation(request, house_id, room_no, check_in, check_out, guests):
    if request.method == 'GET':
        dateFormat = '%d-%b-%Y'
        checkInDate = datetime.strptime(check_in, dateFormat)
        checkOutDate = datetime.strptime(check_out, dateFormat)
        noOfDays = (checkOutDate - checkInDate).days

        data = {
            'house_id': house_id, 
            'room_no': room_no, 
            'check_in': checkInDate.strftime(dateFormat), 
            'check_out': checkOutDate.strftime(dateFormat),
            'guests': guests
        }
        cursor = connection.cursor()

        if request.session.get('username') is not None:
            
            query = """SELECT *
                    FROM USERS 
                    WHERE USERNAME = %s"""
            cursor.execute(query, [request.session['username']])
            result = definitions.dictfetchone(cursor)
            data.update(result)

        query = """SELECT COUNTRY_NAME
                FROM COUNTRIES"""
        cursor.execute(query, [])
        result = definitions.dictfetchall(cursor)
        data.update({
            'countries': result
        })

        query = """SELECT HOUSE_NAME, PATH
                FROM HOUSES JOIN HOUSE_PHOTOS_PATH USING(HOUSE_ID)
                WHERE HOUSE_ID = %s"""
        cursor.execute(query, [house_id])
        result = definitions.dictfetchall(cursor)
        data.update({
            'house': result[0]
        })

        query = """SELECT PRICE, OFFER_PCT
                FROM ROOMS
                WHERE HOUSE_ID = %s AND ROOM_NO = %s"""
        cursor.execute(query, [house_id, room_no])
        result = definitions.dictfetchone(cursor)
        pricePerNight = result['PRICE']
        offer = result['OFFER_PCT']
        data.update({
            'room': result
        })

        totalPrice = pricePerNight * noOfDays
        totalOffer = totalPrice * (offer / 100)
        data.update({
            'daysReserving': noOfDays,
            'totalPrice':  totalPrice,
            'totalOffer': totalOffer,
            'totalPriceWithOffer': totalPrice - totalOffer
        })
        cursor.close()
            
        return render(request, 'pages/reservation.html', data)

    elif request.method == 'POST':
        amount = request.POST['price']
        paymentMethod = request.POST.get(
            'paymentMethod', 'Credit or debit card')
        username = request.session['username']
        houseId = request.POST['houseid']
        roomno = request.POST['roomno']
        checkInDate = request.POST['checkin']
        checkOutDate = request.POST['checkout']
        transactionTime = datetime.now().strftime("%d%m%Y%H%M%S")
        # transaction id format = userid-houseid-roomno-ddmmyyyyhhmmss
        transactionId = str(userId) + '-' + str(houseId) + '-' + str(roomno) + '-' + str(transactionTime)

        cursor = connection.cursor()
        query = """SELECT USER_ID FROM USERS WHERE USERNAME = %s"""
        cursor.execute(query, [username])
        userId = cursor.fetchone()[0]
        print(userId, houseId, roomno, transactionId, checkInDate, checkOutDate)

        query = """INSERT INTO PAYMENTS VALUES(%s, SYSDATE, %s, %s)"""
        try:
            cursor.execute(query, [transactionId, amount, paymentMethod])

            query = """INSERT INTO RENTS(USER_ID, HOUSE_ID, ROOM_NO, TRANSACTION_ID, CHECKIN, CHECKOUT)
                    VALUES(%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, [userId, houseId, roomno, transactionId, checkInDate, checkOutDate])
            messages.success(request, "Your reservation was successful")
        except IntegrityError:
            print('Transaction Id is not unique')
            messages.error(request, "Server Error.")
        
        # TODO: redirect to all the rents page of the user
        return redirect('home')
