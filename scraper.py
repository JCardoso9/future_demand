import requests
from bs4 import BeautifulSoup
import re


def parse_elements(job_elements):
    events = []
    for je in job_elements[1:]:

        date = je.attrs["data-date"]
        event_id = je.attrs["id"].split("event_id_")[1]

        date_place = je.find("div", class_="date-place")
        time_div = date_place.find("div", class_="right")
        times = time_div.find("span", class_="time").text.split("/")

        location = date_place.find("p", class_="location").text.strip()

        image_style = je.find("div", class_="image").attrs["style"]
        image_link = re.search(r"\((.*?)\)", image_style).group(0)[1:-1]

        event_info = je.find("div", class_="event-info").find("div", class_="wi")
        surtitle = event_info.find("p", class_="surtitle").text.strip()
        artists = event_info.find("p", class_="title").text.strip()
        subtitle = event_info.find("p", class_="subtitle")
        sponsor = subtitle.find("span", class_="sponsor")
        if sponsor is not None:
            sponsor_txt = sponsor.text.strip()
        else:
            sponsor_txt = ""
        composers, *_ = subtitle.text.strip().split("\n")

        if composers == sponsor_txt:
            composers = ""

        for time in times:
            info = {
                "surtitle": surtitle,
                "artists": artists,
                "composers": composers,
                "img_link": image_link,
                "sponsor": sponsor_txt,
                "location":location,
                "date": date,
                "event_id": event_id,
                "time": time,
            }
            events.append(info)

    return events





def scrape_source(link):

    URL = link
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="event-list")
    job_elements = results.find_all("div", class_="entry")

    events = parse_elements(job_elements)
    return events







