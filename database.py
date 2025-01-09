import sqlite3

def create_database():
    conn = sqlite3.connect('event_management.db')
    cursor = conn.cursor()

    # Create Venues table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Venues (
            VenueID INTEGER PRIMARY KEY AUTOINCREMENT,
            VenueName TEXT NOT NULL,
            Location TEXT NOT NULL,
            Capacity INTEGER NOT NULL
        )
    ''')

    # Create Events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events (
            EventID INTEGER PRIMARY KEY AUTOINCREMENT,
            EventName TEXT NOT NULL,
            EventDate TEXT NOT NULL,
            VenueID INTEGER NOT NULL,
            TicketPrice REAL NOT NULL,
            FOREIGN KEY (VenueID) REFERENCES Venues(VenueID)
        )
    ''')

    # Create Attendees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendees (
            AttendeeID INTEGER PRIMARY KEY AUTOINCREMENT,
            AttendeeName TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE
        )
    ''')

    # Create Tickets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tickets (
            TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
            EventID INTEGER NOT NULL,
            AttendeeID INTEGER NOT NULL,
            Price REAL NOT NULL,
            FOREIGN KEY (EventID) REFERENCES Events(EventID),
            FOREIGN KEY (AttendeeID) REFERENCES Attendees(AttendeeID)
        )
    ''')

    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('event_management.db')
