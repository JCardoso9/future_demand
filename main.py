from flask import Flask
from db_connector import query_database, insert_events
from ploter import plot_dates
from scraper import scrape_source


app = Flask(__name__)


@app.route('/')
def show_index():
    print("Scraping")
    events = scrape_source("https://www.lucernefestival.ch/en/program/summer-festival-22")

    insert_events(events)
    query = "SELECT date(Event_date), Count(*) as counted FROM events GROUP BY date(Event_date) ORDER BY date(Event_date)"
    dates = query_database(query)
    print(dates)

    data = plot_dates(dates)

    return f"<img src='data:image/png;base64,{data}'/>"

if __name__ == '__main__':
    app.run(host='0.0.0.0')