from django.shortcuts import render
from django.db import connection, IntegrityError
from rentastay import definitions
# Create your views here.

def home(request):
    cursor = connection.cursor()
    query = """SELECT HOUSE_NAME, CITY_NAME, STATE_NAME, COUNTRY_NAME
                FROM HOUSES JOIN ADDRESSES USING(ADDRESS_ID) 
                JOIN CITIES USING(CITY_ID) 
                JOIN STATES USING(STATE_ID) 
                JOIN COUNTRIES USING(COUNTRY_NAME)"""
    cursor.execute(query)
    result = definitions.dictfetchall(cursor)
    cursor.close()
    data = {'houses':result}
    
    return render(request, 'pages/home.html', data)
