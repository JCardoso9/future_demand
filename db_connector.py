import psycopg2
import os

params = {
    "dbname": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get('POSTGRES_USER'),
    "host": os.environ.get('POSTGRES_HOST'),
    "password": os.environ.get('POSTGRES_PASSWORD')
}

def insert_events(events):
    try:
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        for event in events:
            print("------------------")
            print(event)
            postgres_insert_query = \
                """ 
                INSERT INTO events (Event_id, Artists, Composers,Surtitle, Sponsor, Location, Img_Link, Event_date) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s) 
                """

            record_to_insert = (
                event["event_id"],
                event["artists"],
                event["composers"],
                event["surtitle"],
                event["sponsor"],
                event["location"],
                event["img_link"],
                f"{event['date']} {event['time'].replace('.', ':')}",
                
            )
            cursor.execute(postgres_insert_query, record_to_insert)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into table")


    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def query_database(query):
    """ query data from the vendors table """
    dates = {}
    conn = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        row = cur.fetchone()

        while row is not None:
            dates[row[0]] = row[1]
            row = cur.fetchone()
            
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return dates


