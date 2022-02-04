from django.db import connection

# dictfetchall converts cursor array based output to dict
def dictfetchall(cursor):
    # Get all the row data from the cursor and convert it into a dictionary
    fetchedData = cursor.fetchall()
    if fetchedData is None:
        return None
    
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in fetchedData
    ]

def dictfetchone(cursor):
    fetchedData = cursor.fetchone()
    if fetchedData is None:
        return None
    
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, fetchedData))
