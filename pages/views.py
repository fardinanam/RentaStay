from asyncio.windows_events import NULL
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
    result = definitions.dictfetchall(cursor)
    cursor.close()

    return result

def getYourHouses(request):
    cursor = connection.cursor()
    query = "SELECT USER_ID FROM USERS WHERE USERNAME=%s"
    if 'username' not in request.session:
        return redirect('home')
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
    return render(request, 'pages/home.html', data)

def yourhouses(request):
    houses = getYourHouses(request)
    data = {'houses':houses}
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

def getJsonAvailableRoomsData(request, house_id, check_in, check_out, guests):
    cursor = connection.cursor()
    query = """SELECT * FROM ROOMS R
            WHERE HOUSE_ID = %s
            AND ROOM_NO NOT IN (
                SELECT ROOM_NO FROM RENTS
                WHERE HOUSE_ID = R.HOUSE_ID
                AND ((TO_DATE(%s, 'DD-MON-YYYY') BETWEEN CHECKIN AND CHECKOUT)
                OR (TO_DATE(%s, 'DD-MON-YYYY') BETWEEN CHECKIN AND CHECKOUT)
                OR (CHECKIN BETWEEN TO_DATE(%s, 'DD-MON-YYYY') AND TO_DATE(%s, 'DD-MON-YYYY'))))
            AND MAX_CAPACITY >= %s"""
    cursor.execute(query, [house_id, check_in, check_out, check_in, check_out, guests])
    rooms = definitions.dictfetchall(cursor)
    rooms = sorted(rooms, key=lambda i: i['ROOM_NO'])

    return JsonResponse({'rooms': rooms})

def updateReview(request, rent_id, owner_rating, house_rating, owner_review, house_review):
    if request.session.has_key('username') is False:
        return redirect('/')

    cursor = connection.cursor()
    query = """UPDATE RENTS
            SET OWNER_RATING = %s,
            OWNER_REVIEW = %s,
            HOUSE_RATING = %s,
            HOUSE_REVIEW = %s,
            REVIEW_DATE = SYSDATE
            WHERE RENT_ID = %s;"""
    try:
        cursor.execute(query, [owner_rating, owner_review, house_rating, house_review, rent_id])
        cursor.close()
        return JsonResponse({'message': 'True'})
    except Exception as e:
        return JsonResponse({'message': 'False'})

def house(request, house_id):
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

    houseFeatures = result["FEATURES"]

    if((houseFeatures is not None) and (houseFeatures is not NULL)):
        houseFeatures = houseFeatures.split("\\")
        del houseFeatures[-1]
        result.update({
            'HOUSE_FEATURES': houseFeatures
        })

    minPrice = cursor.callfunc('GET_MIN_PRICE', float, [house_id])
    maxPrice = cursor.callfunc('GET_MAX_PRICE', float, [house_id])

    result.update({
        'MIN_PRICE': minPrice,
        'MAX_PRICE': maxPrice
    })

    query = """SELECT PATH
            FROM HOUSE_PHOTOS_PATH
            WHERE HOUSE_ID = %s"""
    cursor.execute(query, [house_id])
    photosPath = definitions.dictfetchall(cursor)

    query = """SELECT TRUNC(AVG(HOUSE_RATING), 2) AVG_HOUSE_RATING, 
            COUNT(HOUSE_RATING) TOTAL_HOUSE_REVIEWS
            FROM RENTS
            WHERE HOUSE_ID = %s;"""
    cursor.execute(query, [house_id])
    reviews = definitions.dictfetchone(cursor)
    result.update(reviews)

    query = """SELECT FIRST_NAME, HOUSE_RATING, HOUSE_REVIEW, 
            PROFILE_PIC, REVIEW_DATE
            FROM RENTS JOIN USERS USING(USER_ID)
            WHERE HOUSE_ID = %s AND HOUSE_REVIEW IS NOT NULL;"""
    cursor.execute(query, [house_id])
    reviews = definitions.dictfetchall(cursor)

    query = """SELECT TRUNC(AVG(OWNER_RATING), 2) AVG_OWNER_RATING, COUNT(OWNER_RATING) TOTAL_OWNER_RATING
            FROM RENTS
            WHERE HOUSE_ID IN (
            SELECT HOUSE_ID
            FROM HOUSES
            WHERE USER_ID = (
            SELECT USER_ID
            FROM HOUSES
            WHERE HOUSE_ID = %s
            ))"""
    cursor.execute(query, [house_id])
    ownerRating = definitions.dictfetchone(cursor)
    cursor.close()

    return render(request, 'pages/house.html', {'house':result, 'reviews': reviews, 'owner_rating':ownerRating, 'photos_url': photosPath})

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
            query = """SELECT USERNAME FROM USERS
                    JOIN HOUSES USING(USER_ID)
                    WHERE HOUSE_ID = %s;"""
            cursor.execute(query, [house_id])
            houseOwner = cursor.fetchone()[0]
            if houseOwner == request.session['username']:
                messages.error(request, 'You can\'t rent your own house')
                return redirect('/house/' + str(house_id))

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
        totalOffer = round(totalPrice * (offer / 100))
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
        guests = request.POST['guests']

        cursor = connection.cursor()

        isAvailable = cursor.callfunc('IS_ROOM_AVAILABLE', str, [house_id, room_no, checkInDate, checkOutDate, guests])

        if isAvailable == 'N':
            messages.error(request, 'Sorry! This room is not available in this criteria.')
            return redirect('/')

        query = """SELECT USER_ID FROM USERS WHERE USERNAME = %s"""
        cursor.execute(query, [username])
        userId = cursor.fetchone()[0]

        transactionTime = datetime.now().strftime("%d%m%Y%H%M%S")
        transactionId = str(userId) + '-' + str(houseId) + '-' + str(roomno) + '-' + str(transactionTime)

        query = """INSERT INTO PAYMENTS VALUES(%s, SYSDATE, %s, %s)"""
        try:
            cursor.execute(query, [transactionId, amount, paymentMethod])

            query = """INSERT INTO RENTS(USER_ID, HOUSE_ID, ROOM_NO, TRANSACTION_ID, CHECKIN, CHECKOUT)
                    VALUES(%s, %s, %s, %s, TO_DATE(%s, \'DD-Mon-YYYY\'), TO_DATE(%s, \'DD-Mon-YYYY\'))"""
            cursor.execute(query, [userId, houseId, roomno, transactionId, checkInDate, checkOutDate])
            messages.success(request, "Your reservation was successful")
        except IntegrityError:
            messages.error(request, "Server Error.")
        
        return redirect('/myRents/')

def myRents(request):
    if request.session.has_key('username') is False:
        messages.error(request, "You must be logged in to see your rents")
        return redirect('/accounts/signin/')
    
    username = request.session.get('username')
    cursor = connection.cursor()

    query = """SELECT USER_ID 
            FROM USERS
            WHERE USERNAME = %s"""
    cursor.execute(query, [username])
    userId = cursor.fetchone()[0]

    query = """SELECT RENT_ID, HOUSE_ID, HOUSE_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            HOUSE_NO, STREET, POST_CODE, CITY_NAME, STATE_NAME, COUNTRY_NAME,
            USERNAME, FIRST_NAME, LAST_NAME, HOUSE_RATING, HOUSE_REVIEW, OWNER_RATING, OWNER_REVIEW
            FROM RENTS R
            JOIN HOUSES H USING(HOUSE_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN CITIES USING (CITY_ID)
            JOIN STATES USING (STATE_ID)
            JOIN COUNTRIES USING (COUNTRY_NAME)
            JOIN USERS O ON (H.USER_ID = O.USER_ID)
            WHERE R.USER_ID = %s 
            AND CHECKOUT < SYSDATE;"""
    cursor.execute(query, [userId])
    olderRents = definitions.dictfetchall(cursor)

    query = """SELECT RENT_ID, HOUSE_ID, HOUSE_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            HOUSE_NO, STREET, POST_CODE, CITY_NAME, STATE_NAME, COUNTRY_NAME,
            USERNAME, FIRST_NAME, LAST_NAME, HOUSE_RATING, HOUSE_REVIEW, OWNER_RATING, OWNER_REVIEW
            FROM RENTS R
            JOIN HOUSES H USING(HOUSE_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN CITIES USING (CITY_ID)
            JOIN STATES USING (STATE_ID)
            JOIN COUNTRIES USING (COUNTRY_NAME)
            JOIN USERS O ON (H.USER_ID = O.USER_ID)
            WHERE R.USER_ID = %s 
            AND SYSDATE BETWEEN CHECKIN AND CHECKOUT;"""
    cursor.execute(query, [userId])
    ongoingRents = definitions.dictfetchall(cursor)

    query = """SELECT RENT_ID, HOUSE_ID, HOUSE_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            HOUSE_NO, STREET, POST_CODE, CITY_NAME, STATE_NAME, COUNTRY_NAME,
            USERNAME, FIRST_NAME, LAST_NAME, HOUSE_RATING, HOUSE_REVIEW, OWNER_RATING, OWNER_REVIEW
            FROM RENTS R
            JOIN HOUSES H USING(HOUSE_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN CITIES USING (CITY_ID)
            JOIN STATES USING (STATE_ID)
            JOIN COUNTRIES USING (COUNTRY_NAME)
            JOIN USERS O ON (H.USER_ID = O.USER_ID)
            WHERE R.USER_ID = %s 
            AND CHECKIN > SYSDATE;"""
    cursor.execute(query, [userId])
    upcomingRents = definitions.dictfetchall(cursor)

    cursor.close()

    if len(ongoingRents) == 0:
        ongoingRents = None
    if len(olderRents) == 0:
        olderRents = None
    if len(upcomingRents) == 0:
        upcomingRents = None

    data = {
        'older_rents': olderRents,
        'ongoing_rents': ongoingRents,
        'upcoming_rents': upcomingRents
    }

    return render(request, 'pages/myrents.html', data)

def myGuests(request):
    if request.session.has_key('username') is False:
        messages.error(request, "You must be logged in to see your rents")
        return redirect('/accounts/signin/')
    
    username = request.session.get('username')
    cursor = connection.cursor()
    
    query = """SELECT USER_ID 
            FROM USERS
            WHERE USERNAME = %s"""
    cursor.execute(query, [username])
    userId = cursor.fetchone()[0]

    query = """SELECT INITCAP(HOUSE_NAME) HOUSE_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            HOUSE_NO, STREET, POST_CODE, CITY_NAME, STATE_NAME, COUNTRY_NAME,
            FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, JOIN_DATE, PROFILE_PIC
            FROM RENTS
            JOIN USERS USING(USER_ID)
            JOIN HOUSES USING(HOUSE_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN CITIES USING (CITY_ID)
            JOIN STATES USING (STATE_ID)
            JOIN COUNTRIES USING (COUNTRY_NAME)
            WHERE HOUSE_ID IN (
            SELECT HOUSE_ID
            FROM HOUSES
            WHERE USER_ID = %s)
            AND SYSDATE BETWEEN CHECKIN AND CHECKOUT;"""
    cursor.execute(query, [userId])
    currentGuests = definitions.dictfetchall(cursor)

    query = """SELECT INITCAP(HOUSE_NAME) HOUSE_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            HOUSE_NO, STREET, POST_CODE, CITY_NAME, STATE_NAME, COUNTRY_NAME,
            FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, JOIN_DATE, PROFILE_PIC
            FROM RENTS
            JOIN USERS USING(USER_ID)
            JOIN HOUSES USING(HOUSE_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN CITIES USING (CITY_ID)
            JOIN STATES USING (STATE_ID)
            JOIN COUNTRIES USING (COUNTRY_NAME)
            WHERE HOUSE_ID IN (
            SELECT HOUSE_ID
            FROM HOUSES
            WHERE USER_ID = %s)
            AND SYSDATE > CHECKOUT;"""
    cursor.execute(query, [userId])
    olderGuests = definitions.dictfetchall(cursor)

    query = """SELECT INITCAP(HOUSE_NAME) HOUSE_NAME, ROOM_NO, CHECKIN, CHECKOUT, 
            HOUSE_NO, STREET, POST_CODE, CITY_NAME, STATE_NAME, COUNTRY_NAME,
            FIRST_NAME, LAST_NAME, EMAIL, PHONE_NO, JOIN_DATE, PROFILE_PIC
            FROM RENTS
            JOIN USERS USING(USER_ID)
            JOIN HOUSES USING(HOUSE_ID)
            JOIN ADDRESSES USING(ADDRESS_ID)
            JOIN CITIES USING (CITY_ID)
            JOIN STATES USING (STATE_ID)
            JOIN COUNTRIES USING (COUNTRY_NAME)
            WHERE HOUSE_ID IN (
            SELECT HOUSE_ID
            FROM HOUSES
            WHERE USER_ID = %s)
            AND SYSDATE < CHECKIN;"""
    cursor.execute(query, [userId])
    upcomingGuests = definitions.dictfetchall(cursor)
    cursor.close()

    if len(currentGuests) == 0:
        currentGuests = None
    if len(olderGuests) == 0:
        olderGuests = None
    if len(upcomingGuests) == 0:
        upcomingGuests = None

    data = {
        'older_guests': olderGuests,
        'current_guests': currentGuests,
        'upcoming_guests': upcomingGuests
    }

    return render(request, 'pages/myguests.html', data)
