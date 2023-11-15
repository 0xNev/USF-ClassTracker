import sqlite3


conn = sqlite3.connect('database.db')
conn.execute("""CREATE TABLE classes (
    status TEXT NOT NULL,
    crn TEXT NOT NULL,
    subj TEXT NOT NULL,
    crse TEXT NOT NULL,
    sec TEXT NOT NULL,
    cred TEXT NOT NULL,
    title TEXT NOT NULL,
    instructional_method TEXT NOT NULL,
    permit_req TEXT NOT NULL,
    term_dates TEXT NOT NULL,
    days TEXT NOT NULL,
    time TEXT NOT NULL,
    seats_cap TEXT NOT NULL,
    seats_avail TEXT NOT NULL,
    waitlist_cap TEXT NOT NULL,
    waitlist_avail TEXT NOT NULL,
    instructor TEXT NOT NULL,
    campus TEXT NOT NULL,
    location TEXT NOT NULL,
    attribute TEXT NOT NULL,
    PRIMARY KEY (crn)
    
);""")


conn.commit()
conn.close()

