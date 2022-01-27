from django.shortcuts import render
from django.db import connection, IntegrityError

# Create your views here.

def home(request):
    cursor = connection.cursor()
    query = "SELECT * FROM HOUSES"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    data = {'houses':result}
    
    return render(request, 'pages/home.html', data)
