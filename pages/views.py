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

def house(request):
    houseId = request.GET['houseId']
    # print(f"house id from GET is {houseId}")
    cursor = connection.cursor()
    query = """SELECT * 
            FROM HOUSES JOIN USERS USING(USER_ID)
            WHERE HOUSE_ID = %s"""
    cursor.execute(query, [houseId])
    result = definitions.dictfetchone(cursor)
    cursor.close()

    return render(request, 'pages/house.html', {'house':result})