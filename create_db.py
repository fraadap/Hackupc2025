import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS User (
    email TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS GroupTable (
    code INTEGER PRIMARY KEY 
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS UGroup (
    email TEXT NOT NULL,
    code INTEGER NOT NULL,
    PRIMARY KEY (email, code),
    FOREIGN KEY (email) REFERENCES User(email),
    FOREIGN KEY (code) REFERENCES GroupTable(code)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS City (
    name TEXT PRIMARY KEY
)
""")

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS Flight (
    code INTEGER PRIMARY KEY NOT NULL,
    cost FLOAT NOT NULL,
    depCity TEXT NOT NULL,
    arrCity TEXT NOT NULL,
    depTime TEXT NOT NULL,
    arrTime TEXT NOT NULL,

    FOREIGN KEY (depCity) REFERENCES City(name),
    FOREIGN KEY (arrCity) REFERENCES City(name)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Category (
    name TEXT PRIMARY KEY NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS CityCateg (
    city TEXT NOT NULL,
    category TEXT NOT NULL,
    descr TEXT NOT NULL,
               
    PRIMARY KEY(city, category),
    FOREIGN KEY (city) REFERENCES City(name),
    FOREIGN KEY (category) REFERENCES Category(name)     
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS CityCateg (
    city TEXT NOT NULL,
    category TEXT NOT NULL,
    descr TEXT NOT NULL,
               
    PRIMARY KEY(city, category),
    FOREIGN KEY (city) REFERENCES City(name),
    FOREIGN KEY (category) REFERENCES Category(name)       
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ImportanceUC (
    email TEXT NOT NULL,
    category TEXT NOT NULL,
    importance INTEGER NOT NULL CHECK (importance IN (0, 10)),
               
    PRIMARY KEY(email, category),
    FOREIGN KEY (email) REFERENCES User(email),
    FOREIGN KEY (category) REFERENCES Category(name)        
)
""")

#cursor.execute("INSERT INTO User (username, email) VALUES (?, ?)", ("Mario Rossi", "mario@example.com"))

cursor.execute("SELECT * FROM User")
for riga in cursor.fetchall():
    print(riga)

# 5. Salva e chiudi
conn.commit()
conn.close()
