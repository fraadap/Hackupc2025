import sqlite3
import os

# Create database directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('data/reunion.db')
cursor = conn.cursor()

# Create User table
cursor.execute("""
CREATE TABLE IF NOT EXISTS User (
    email TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# Create GroupTable table
cursor.execute("""
CREATE TABLE IF NOT EXISTS GroupTable (
    code INTEGER PRIMARY KEY 
)
""")

# Create UGroup table (many-to-many relationship between users and groups)
cursor.execute("""
CREATE TABLE IF NOT EXISTS UGroup (
    email TEXT NOT NULL,
    code INTEGER NOT NULL,
    PRIMARY KEY (email, code),
    FOREIGN KEY (email) REFERENCES User(email),
    FOREIGN KEY (code) REFERENCES GroupTable(code)
)
""")

# Create City table
cursor.execute("""
CREATE TABLE IF NOT EXISTS City (
    name TEXT PRIMARY KEY
)
""")

# Create VoteUC table (stores votes of users for cities)
cursor.execute("""
CREATE TABLE IF NOT EXISTS VoteUC (
    email TEXT NOT NULL,
    city TEXT NOT NULL,
    value INTEGER NOT NULL CHECK (value IN (0, 1)),
    PRIMARY KEY (email, city),
    FOREIGN KEY (email) REFERENCES User(email),
    FOREIGN KEY (city) REFERENCES City(name)
)
""")

# Create FlightCompany table
cursor.execute("""
CREATE TABLE IF NOT EXISTS FlightCompany (
    name TEXT PRIMARY KEY NOT NULL
)
""")

# Create Flight table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Flight (
    code INTEGER PRIMARY KEY NOT NULL,
    cost FLOAT NOT NULL,
    depCity TEXT NOT NULL,
    arrCity TEXT NOT NULL,
    depTime TEXT NOT NULL,
    timeDuration INTEGER NOT NULL,
    distance FLOAT NOT NULL,
    planeModel TEXT NOT NULL,
    company TEXT NOT NULL,
    FOREIGN KEY (depCity) REFERENCES City(name),
    FOREIGN KEY (arrCity) REFERENCES City(name),
    FOREIGN KEY (company) REFERENCES FlightCompany(name)
)
""")

# Create Category table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Category (
    name TEXT PRIMARY KEY NOT NULL
)
""")

# Create CityCateg table (values of categories for cities)
cursor.execute("""
CREATE TABLE IF NOT EXISTS CityCateg (
    city TEXT NOT NULL,
    category TEXT NOT NULL,
    descr TEXT NOT NULL,
    value INTEGER NOT NULL CHECK (value BETWEEN 1 AND 10),
    PRIMARY KEY(city, category),
    FOREIGN KEY (city) REFERENCES City(name),
    FOREIGN KEY (category) REFERENCES Category(name)     
)
""")

# Create ImportanceUC table (importance of categories for users)
cursor.execute("""
CREATE TABLE IF NOT EXISTS ImportanceUC (
    email TEXT NOT NULL,
    category TEXT NOT NULL,
    importance INTEGER NOT NULL CHECK (importance BETWEEN 1 AND 10),
    PRIMARY KEY(email, category),
    FOREIGN KEY (email) REFERENCES User(email),
    FOREIGN KEY (category) REFERENCES Category(name)        
)
""")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database schema created successfully!") 