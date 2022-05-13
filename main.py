from flask import Flask
from db_connector import query_database, create_table, insert_events
from ploter import plot_dates
from scraper import scrape_source



app = Flask(__name__)

create_table_query ="""
        CREATE TABLE events (
            Event_id INTEGER,
            Artists TEXT,
            Composers TEXT,
            Surtitle TEXT,
            Sponsor TEXT,
            Location TEXT,
            Img_Link TEXT,
            Event_date TIMESTAMP,
            PRIMARY KEY (Event_id, Event_date)
        )
    """

@app.route('/')
@app.route('/index')
def show_index():
    events = scrape_source("https://www.lucernefestival.ch/en/program/summer-festival-22")

    create_table(create_table_query)
    insert_events(events)
    query = "SELECT date(Event_date), Count(*) as counted FROM events GROUP BY date(Event_date) ORDER BY date(Event_date)"
    dates = query_database(query)

    data = plot_dates(dates)

    return f"<img src='data:image/png;base64,{data}'/>"