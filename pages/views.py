from django.shortcuts import render
from django.db import connection, IntegrityError
from rentastay import definitions
from django.http import JsonResponse

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

def home(request):
    houses = getHouses()
    data = {'houses':houses}
    # print(houses)
    return render(request, 'pages/home.html', data)

def getJsonHouseData(request):
    houses = getHouses()

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

def house(request, house_id):
    # print(f"house id from GET is {houseId}")
    cursor = connection.cursor()
    query = """SELECT * 
            FROM HOUSES JOIN USERS USING(USER_ID)
            WHERE HOUSE_ID = %s"""
    cursor.execute(query, [house_id])
    result = definitions.dictfetchone(cursor)
    cursor.close()

    return render(request, 'pages/house.html', {'house':result})