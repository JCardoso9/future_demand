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
);