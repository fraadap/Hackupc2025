import sqlite3
import os

# Create database directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('data/reunion.db')
cursor = conn.cursor()

# Drop tables if they exist (for easy recreation during development)
cursor.execute("DROP TABLE IF EXISTS Image")
cursor.execute("DROP TABLE IF EXISTS VoteUC")
cursor.execute("DROP TABLE IF EXISTS CityCateg")
cursor.execute("DROP TABLE IF EXISTS ImportanceUC")
cursor.execute("DROP TABLE IF EXISTS UGroup")
cursor.execute("DROP TABLE IF EXISTS Flight")
cursor.execute("DROP TABLE IF EXISTS GroupTable")
cursor.execute("DROP TABLE IF EXISTS Category")
cursor.execute("DROP TABLE IF EXISTS FlightCompany")
cursor.execute("DROP TABLE IF EXISTS City")
cursor.execute("DROP TABLE IF EXISTS User")

print("Existing tables dropped (if any).")

# User Table
cursor.execute("""
CREATE TABLE User (
    email TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# City Table
cursor.execute("""
CREATE TABLE City (
    name TEXT PRIMARY KEY
)
""")

# Category Table
cursor.execute("""
CREATE TABLE Category (
    name TEXT PRIMARY KEY
)
""")

# CityCateg Table (City Features/Attributes)
cursor.execute("""
CREATE TABLE CityCateg (
    city TEXT,
    category TEXT,
    descr TEXT,
    value INTEGER CHECK(value >= 1 AND value <= 10),
    PRIMARY KEY (city, category),
    FOREIGN KEY (city) REFERENCES City(name) ON DELETE CASCADE,
    FOREIGN KEY (category) REFERENCES Category(name) ON DELETE CASCADE
)
""")

# --- Add Image Table --- 
cursor.execute("""
CREATE TABLE Image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL, 
    image_data BLOB NOT NULL,         -- Stores binary image data
    content_type TEXT NOT NULL,       -- Stores MIME type (e.g., 'image/jpeg')
    "order" INTEGER NOT NULL,           -- Order of the image (1, 2, 3)
    FOREIGN KEY (city_name) REFERENCES City(name) ON DELETE CASCADE,
    UNIQUE(city_name, "order")        -- Ensure only 3 images per city in order
)
""")
print("Created Image table.")
# --- End Image Table --- 

# ImportanceUC Table (User Preferences)
cursor.execute("""
CREATE TABLE ImportanceUC (
    email TEXT,
    category TEXT,
    importance INTEGER CHECK(importance >= 1 AND importance <= 10),
    PRIMARY KEY (email, category),
    FOREIGN KEY (email) REFERENCES User(email) ON DELETE CASCADE,
    FOREIGN KEY (category) REFERENCES Category(name) ON DELETE CASCADE
)
""")

# VoteUC Table (User Votes on Cities)
cursor.execute("""
CREATE TABLE VoteUC (
    email TEXT,
    city TEXT,
    value INTEGER CHECK(value IN (0, 1)), -- 0 dislike, 1 like
    PRIMARY KEY (email, city),
    FOREIGN KEY (email) REFERENCES User(email) ON DELETE CASCADE,
    FOREIGN KEY (city) REFERENCES City(name) ON DELETE CASCADE
)
""")

# Group Table
cursor.execute("""
CREATE TABLE GroupTable (
    code INTEGER PRIMARY KEY
)
""")

# UGroup Table (User-Group Membership)
cursor.execute("""
CREATE TABLE UGroup (
    email TEXT,
    code INTEGER,
    PRIMARY KEY (email, code),
    FOREIGN KEY (email) REFERENCES User(email) ON DELETE CASCADE,
    FOREIGN KEY (code) REFERENCES GroupTable(code) ON DELETE CASCADE
)
""")

# Flight Company Table
cursor.execute("""
CREATE TABLE FlightCompany (
    name TEXT PRIMARY KEY
)
""")

# Flight Table
cursor.execute("""
CREATE TABLE Flight (
    code INTEGER PRIMARY KEY,
    cost REAL,
    depCity TEXT,
    arrCity TEXT,
    depTime TEXT, -- ISO format string
    timeDuration INTEGER, -- in minutes
    distance REAL, -- in km
    planeModel TEXT,
    company TEXT,
    FOREIGN KEY (depCity) REFERENCES City(name) ON DELETE SET NULL, 
    FOREIGN KEY (arrCity) REFERENCES City(name) ON DELETE SET NULL,
    FOREIGN KEY (company) REFERENCES FlightCompany(name) ON DELETE SET NULL
)
""")

print("Database tables created successfully.")

# Commit changes and close connection
conn.commit()
conn.close() 