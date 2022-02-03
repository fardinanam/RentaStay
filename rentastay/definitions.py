from django.db import connection

# dictfetchall converts cursor array based output to dict
def dictfetchall(cursor):
    # Get all the row data from the cursor and convert it into a dictionary
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dictfetchone(cursor):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))
