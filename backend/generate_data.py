import sqlite3
import os
import random
import datetime
import hashlib
import traceback
from faker import Faker
import math

# Initialize Faker
fake = Faker()

# Create database directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect('data/reunion.db')
cursor = conn.cursor()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Clear existing data (for repeated runs)
tables = [
    "ImportanceUC", "VoteUC", "UGroup", "Flight", 
    "CityCateg", "User", "City", "Category", 
    "FlightCompany", "GroupTable"
]

for table in tables:
    cursor.execute(f"DELETE FROM {table}")
    
print("Data cleared from all tables. Starting data generation...")

# ------------------------- CATEGORIES -------------------------
# Create categories
categories = [
    {"name": "Food", "emoji": "🍽️"},
    {"name": "CostOfLiving", "emoji": "💰"},
    {"name": "ApartmentCosts", "emoji": "🏠"},
    {"name": "Tranquility", "emoji": "🧘"},
    {"name": "History", "emoji": "🏛️"},
    {"name": "Beach", "emoji": "🏖️"},
    {"name": "Mountains", "emoji": "⛰️"},
    {"name": "Sports", "emoji": "🏅"},
    {"name": "Nature", "emoji": "🌳"},
    {"name": "Adventures", "emoji": "🧗"},
    {"name": "Entertainment", "emoji": "🎭"},
    {"name": "Nightlife", "emoji": "🌃"},
    {"name": "Shopping", "emoji": "🛍️"},
    {"name": "Art", "emoji": "🎨"},
    {"name": "Museums", "emoji": "🏛️"}
]

# Insert categories into the database
for category in categories:
    cursor.execute("INSERT INTO Category (name) VALUES (?)", (category["name"],))

print(f"Added {len(categories)} categories.")

# ------------------------- CITIES -------------------------
# Create cities with realistic attributes
cities = [
    "Barcelona", "Paris", "Rome", "Amsterdam", "Berlin", 
    "Prague", "Vienna", "Lisbon", "Madrid", "Budapest",
    "Florence", "Athens", "Venice", "Dublin", "Copenhagen",
    "Stockholm", "Oslo", "Helsinki", "Krakow", "Zagreb",
    "Dubrovnik", "Edinburgh", "Santorini", "Porto", "Brussels",
    "Zurich", "Geneva", "Milan", "Naples", "Valencia"
]

# City-specific attributes for realistic descriptions
city_attributes = {
    "Barcelona": {
        "landmarks": ["Sagrada Familia", "Park Güell", "La Rambla"],
        "food_specialties": ["paella", "tapas", "crema catalana"],
        "neighborhoods": ["Gothic Quarter", "Barceloneta", "Gràcia"]
    },
    "Paris": {
        "landmarks": ["Eiffel Tower", "Louvre Museum", "Notre Dame"],
        "food_specialties": ["croissants", "coq au vin", "crème brûlée"],
        "neighborhoods": ["Montmartre", "Le Marais", "Latin Quarter"]
    },
    "Rome": {
        "landmarks": ["Colosseum", "Vatican City", "Trevi Fountain"],
        "food_specialties": ["pasta carbonara", "pizza romana", "gelato"],
        "neighborhoods": ["Trastevere", "Monti", "Testaccio"]
    },
    "Amsterdam": {
        "landmarks": ["Anne Frank House", "Rijksmuseum", "Canal Ring"],
        "food_specialties": ["stroopwafels", "herring", "bitterballen"],
        "neighborhoods": ["Jordaan", "De Pijp", "Oost"]
    },
    "Berlin": {
        "landmarks": ["Brandenburg Gate", "Berlin Wall", "Museum Island"],
        "food_specialties": ["currywurst", "döner kebab", "pretzels"],
        "neighborhoods": ["Kreuzberg", "Mitte", "Prenzlauer Berg"]
    },
    "Prague": {
        "landmarks": ["Prague Castle", "Charles Bridge", "Old Town Square"],
        "food_specialties": ["goulash", "trdelník", "svíčková"],
        "neighborhoods": ["Old Town", "Lesser Town", "Vinohrady"]
    },
    "Vienna": {
        "landmarks": ["Schönbrunn Palace", "St. Stephen's Cathedral", "Belvedere Palace"],
        "food_specialties": ["wiener schnitzel", "sachertorte", "apfelstrudel"],
        "neighborhoods": ["Innere Stadt", "Leopoldstadt", "Mariahilf"]
    },
    "Lisbon": {
        "landmarks": ["Belém Tower", "Jerónimos Monastery", "São Jorge Castle"],
        "food_specialties": ["pastel de nata", "bacalhau", "caldo verde"],
        "neighborhoods": ["Alfama", "Bairro Alto", "Chiado"]
    },
    "Madrid": {
        "landmarks": ["Royal Palace", "Prado Museum", "Plaza Mayor"],
        "food_specialties": ["cocido madrileño", "churros", "tortilla española"],
        "neighborhoods": ["Malasaña", "Salamanca", "La Latina"]
    },
    "Budapest": {
        "landmarks": ["Parliament Building", "Fisherman's Bastion", "Chain Bridge"],
        "food_specialties": ["goulash", "langos", "chimney cake"],
        "neighborhoods": ["Castle Hill", "Jewish Quarter", "Erzsébetváros"]
    },
    "Florence": {
        "landmarks": ["Duomo", "Uffizi Gallery", "Ponte Vecchio"],
        "food_specialties": ["bistecca alla fiorentina", "ribollita", "schiacciata"],
        "neighborhoods": ["Oltrarno", "Santa Croce", "San Lorenzo"]
    },
    "Athens": {
        "landmarks": ["Acropolis", "Parthenon", "Temple of Olympian Zeus"],
        "food_specialties": ["moussaka", "souvlaki", "baklava"],
        "neighborhoods": ["Plaka", "Monastiraki", "Kolonaki"]
    },
    "Venice": {
        "landmarks": ["St. Mark's Square", "Grand Canal", "Rialto Bridge"],
        "food_specialties": ["risotto nero", "cicchetti", "fritole"],
        "neighborhoods": ["San Marco", "Cannaregio", "Dorsoduro"]
    },
    "Dublin": {
        "landmarks": ["Trinity College", "Guinness Storehouse", "Dublin Castle"],
        "food_specialties": ["Irish stew", "boxty", "coddle"],
        "neighborhoods": ["Temple Bar", "Portobello", "Stoneybatter"]
    },
    "Copenhagen": {
        "landmarks": ["Tivoli Gardens", "The Little Mermaid", "Nyhavn"],
        "food_specialties": ["smørrebrød", "Danish pastries", "frikadeller"],
        "neighborhoods": ["Nørrebro", "Vesterbro", "Christianshavn"]
    },
    "Stockholm": {
        "landmarks": ["Vasa Museum", "Royal Palace", "Gamla Stan"],
        "food_specialties": ["meatballs", "kanelbullar", "gravlax"],
        "neighborhoods": ["Gamla Stan", "Södermalm", "Östermalm"]
    },
    "Oslo": {
        "landmarks": ["Viking Ship Museum", "Opera House", "Akershus Fortress"],
        "food_specialties": ["brunost", "fårikål", "raspeballer"],
        "neighborhoods": ["Grünerløkka", "Aker Brygge", "Frogner"]
    },
    "Helsinki": {
        "landmarks": ["Helsinki Cathedral", "Suomenlinna", "Temppeliaukio Church"],
        "food_specialties": ["karjalanpiirakka", "lohikeitto", "korvapuusti"],
        "neighborhoods": ["Kallio", "Punavuori", "Töölö"]
    },
    "Krakow": {
        "landmarks": ["Wawel Castle", "Main Market Square", "St. Mary's Basilica"],
        "food_specialties": ["pierogi", "żurek", "obwarzanek"],
        "neighborhoods": ["Kazimierz", "Old Town", "Podgórze"]
    },
    "Zagreb": {
        "landmarks": ["St. Mark's Church", "Zagreb Cathedral", "Lotrščak Tower"],
        "food_specialties": ["štrukli", "cevapi", "zagorski štrukli"],
        "neighborhoods": ["Upper Town", "Lower Town", "Jarun"]
    },
    "Dubrovnik": {
        "landmarks": ["City Walls", "Rector's Palace", "Stradun"],
        "food_specialties": ["black risotto", "peka", "rožata"],
        "neighborhoods": ["Old Town", "Ploče", "Lapad"]
    },
    "Edinburgh": {
        "landmarks": ["Edinburgh Castle", "Royal Mile", "Arthur's Seat"],
        "food_specialties": ["haggis", "scotch pie", "cranachan"],
        "neighborhoods": ["Old Town", "New Town", "Leith"]
    },
    "Santorini": {
        "landmarks": ["Oia", "Fira", "Akrotiri"],
        "food_specialties": ["fava", "tomatokeftedes", "saganaki"],
        "neighborhoods": ["Oia", "Fira", "Imerovigli"]
    },
    "Porto": {
        "landmarks": ["Dom Luís I Bridge", "Livraria Lello", "Ribeira"],
        "food_specialties": ["francesinha", "tripas à moda do Porto", "bacalhau"],
        "neighborhoods": ["Ribeira", "Baixa", "Foz"]
    },
    "Brussels": {
        "landmarks": ["Grand Place", "Atomium", "Manneken Pis"],
        "food_specialties": ["waffles", "moules-frites", "chocolate"],
        "neighborhoods": ["Grand Place", "Sablon", "European Quarter"]
    },
    "Zurich": {
        "landmarks": ["Lake Zurich", "Grossmünster", "Bahnhofstrasse"],
        "food_specialties": ["fondue", "raclette", "zürcher geschnetzeltes"],
        "neighborhoods": ["Altstadt", "Zürich-West", "Seefeld"]
    },
    "Geneva": {
        "landmarks": ["Jet d'Eau", "Lake Geneva", "CERN"],
        "food_specialties": ["longeole", "malakoff", "chocolate"],
        "neighborhoods": ["Old Town", "Pâquis", "Eaux-Vives"]
    },
    "Milan": {
        "landmarks": ["Duomo di Milano", "Galleria Vittorio Emanuele II", "La Scala"],
        "food_specialties": ["risotto alla milanese", "cotoletta", "panettone"],
        "neighborhoods": ["Brera", "Navigli", "Porta Nuova"]
    },
    "Naples": {
        "landmarks": ["Pompeii", "Mount Vesuvius", "Naples Cathedral"],
        "food_specialties": ["pizza napoletana", "sfogliatella", "ragù"],
        "neighborhoods": ["Centro Storico", "Vomero", "Santa Lucia"]
    },
    "Valencia": {
        "landmarks": ["City of Arts and Sciences", "Valencia Cathedral", "Mercado Central"],
        "food_specialties": ["paella valenciana", "horchata", "fideuà"],
        "neighborhoods": ["El Carmen", "Ruzafa", "Malvarrosa"]
    }
}

# Insert cities into the database
for city in cities:
    cursor.execute("INSERT INTO City (name) VALUES (?)", (city,))

print(f"Added {len(cities)} cities.")

# Category description templates
category_templates = {
    "Food": [
        "{emoji} A culinary paradise! Try the famous {food1} and {food2}. Local restaurants serve authentic dishes that will tantalize your taste buds.",
        "{emoji} The food scene is outstanding with specialties like {food1}. Don't miss trying {food2} at local eateries.",
        "{emoji} Foodies will love the variety of cuisines. The {food1} is a must-try along with traditional {food2}."
    ],
    "CostOfLiving": [
        "{emoji} Very affordable for travelers with budget-friendly options for accommodations and dining.",
        "{emoji} Moderate cost of living compared to other European cities. Daily expenses are reasonable.",
        "{emoji} On the pricier side, but the quality of experiences justifies the cost."
    ],
    "ApartmentCosts": [
        "{emoji} Affordable housing in charming neighborhoods like {neighborhood}.",
        "{emoji} Mid-range apartment prices, especially in areas like {neighborhood}.",
        "{emoji} Premium housing market with luxury options in {neighborhood}."
    ],
    "Tranquility": [
        "{emoji} Peaceful atmosphere with quiet streets and relaxing parks.",
        "{emoji} A good balance of lively areas and tranquil spots to unwind.",
        "{emoji} Bustling city life that never sleeps - perfect for those who love energy."
    ],
    "History": [
        "{emoji} Rich historical heritage with landmarks like {landmark} dating back centuries.",
        "{emoji} History buffs will be captivated by sites such as {landmark} and the surrounding architecture.",
        "{emoji} Walking through the streets is like traveling through time - don't miss {landmark}."
    ],
    "Beach": [
        "{emoji} Stunning beaches with crystal clear waters perfect for swimming and sunbathing.",
        "{emoji} Beautiful coastline with several beaches to explore and enjoy water activities.",
        "{emoji} Limited beach access, but the surrounding water views are still spectacular."
    ],
    "Mountains": [
        "{emoji} Breathtaking mountain views with plenty of hiking trails for all levels.",
        "{emoji} Scenic mountain ranges nearby offering outdoor activities year-round.",
        "{emoji} Some hills and elevated areas, but not known for mountainous terrain."
    ],
    "Sports": [
        "{emoji} Sports enthusiasts will love the facilities and local passion for games and activities.",
        "{emoji} Great sports culture with options for both watching and participating.",
        "{emoji} Home to famous sports venues and teams with regular matches and events."
    ],
    "Nature": [
        "{emoji} Abundant green spaces and parks like {landmark} for nature lovers.",
        "{emoji} Beautiful natural landscapes surrounding the city, perfect for day trips.",
        "{emoji} Urban environment with well-maintained parks offering a touch of nature."
    ],
    "Adventures": [
        "{emoji} Thrilling adventure activities from hiking to water sports nearby.",
        "{emoji} Many tour operators offering exciting excursions and adventure packages.",
        "{emoji} Perfect destination for explorers with unique experiences waiting around every corner."
    ],
    "Entertainment": [
        "{emoji} Vibrant entertainment scene with theaters, cinemas, and music venues.",
        "{emoji} Regular cultural events, festivals, and performances throughout the year.",
        "{emoji} World-class entertainment options from operas to modern concerts."
    ],
    "Nightlife": [
        "{emoji} Buzzing nightlife with clubs and bars open until dawn in {neighborhood}.",
        "{emoji} Cozy pubs and wine bars offering a relaxed evening atmosphere.",
        "{emoji} Diverse nightlife scene catering to all tastes from jazz clubs to dance venues."
    ],
    "Shopping": [
        "{emoji} Shopping paradise with everything from luxury boutiques to charming markets.",
        "{emoji} Unique shopping districts offering local crafts and designer brands.",
        "{emoji} Famous shopping streets like {neighborhood} with international and local stores."
    ],
    "Art": [
        "{emoji} Thriving art scene with galleries and street art throughout {neighborhood}.",
        "{emoji} Home to masterpieces in museums and contemporary art spaces.",
        "{emoji} Artistic atmosphere with regular exhibitions and creative workshops."
    ],
    "Museums": [
        "{emoji} World-class museums housing remarkable collections, including {landmark}.",
        "{emoji} Fascinating museums covering history, art, and science topics.",
        "{emoji} Several specialized museums offering insights into unique aspects of local culture."
    ]
}

# Custom values for cities for each category
city_category_values = {
    "Barcelona": {"Food": 9, "CostOfLiving": 6, "ApartmentCosts": 7, "Tranquility": 5, "History": 8, "Beach": 8, "Mountains": 6, "Sports": 9, "Nature": 6, "Adventures": 7, "Entertainment": 9, "Nightlife": 9, "Shopping": 8, "Art": 9, "Museums": 8},
    "Paris": {"Food": 10, "CostOfLiving": 9, "ApartmentCosts": 10, "Tranquility": 4, "History": 10, "Beach": 1, "Mountains": 1, "Sports": 6, "Nature": 5, "Adventures": 5, "Entertainment": 10, "Nightlife": 8, "Shopping": 10, "Art": 10, "Museums": 10},
    "Rome": {"Food": 9, "CostOfLiving": 7, "ApartmentCosts": 8, "Tranquility": 3, "History": 10, "Beach": 5, "Mountains": 3, "Sports": 7, "Nature": 4, "Adventures": 6, "Entertainment": 8, "Nightlife": 7, "Shopping": 8, "Art": 10, "Museums": 10},
    "Amsterdam": {"Food": 7, "CostOfLiving": 8, "ApartmentCosts": 9, "Tranquility": 6, "History": 8, "Beach": 4, "Mountains": 1, "Sports": 7, "Nature": 6, "Adventures": 7, "Entertainment": 8, "Nightlife": 9, "Shopping": 7, "Art": 8, "Museums": 9},
    "Berlin": {"Food": 8, "CostOfLiving": 6, "ApartmentCosts": 7, "Tranquility": 5, "History": 9, "Beach": 2, "Mountains": 1, "Sports": 7, "Nature": 6, "Adventures": 6, "Entertainment": 10, "Nightlife": 10, "Shopping": 8, "Art": 9, "Museums": 9},
    "Prague": {"Food": 7, "CostOfLiving": 5, "ApartmentCosts": 6, "Tranquility": 5, "History": 9, "Beach": 1, "Mountains": 3, "Sports": 6, "Nature": 5, "Adventures": 6, "Entertainment": 7, "Nightlife": 8, "Shopping": 7, "Art": 8, "Museums": 8},
    "Vienna": {"Food": 8, "CostOfLiving": 7, "ApartmentCosts": 8, "Tranquility": 7, "History": 9, "Beach": 1, "Mountains": 4, "Sports": 6, "Nature": 6, "Adventures": 5, "Entertainment": 9, "Nightlife": 6, "Shopping": 8, "Art": 10, "Museums": 10},
    "Lisbon": {"Food": 8, "CostOfLiving": 5, "ApartmentCosts": 6, "Tranquility": 6, "History": 8, "Beach": 8, "Mountains": 4, "Sports": 6, "Nature": 7, "Adventures": 7, "Entertainment": 7, "Nightlife": 8, "Shopping": 7, "Art": 7, "Museums": 7},
    "Madrid": {"Food": 9, "CostOfLiving": 6, "ApartmentCosts": 7, "Tranquility": 4, "History": 8, "Beach": 1, "Mountains": 5, "Sports": 9, "Nature": 5, "Adventures": 6, "Entertainment": 9, "Nightlife": 10, "Shopping": 8, "Art": 9, "Museums": 10},
    "Budapest": {"Food": 7, "CostOfLiving": 4, "ApartmentCosts": 5, "Tranquility": 5, "History": 8, "Beach": 2, "Mountains": 3, "Sports": 6, "Nature": 5, "Adventures": 7, "Entertainment": 8, "Nightlife": 9, "Shopping": 6, "Art": 7, "Museums": 8},
    "Florence": {"Food": 9, "CostOfLiving": 7, "ApartmentCosts": 8, "Tranquility": 6, "History": 10, "Beach": 3, "Mountains": 5, "Sports": 5, "Nature": 6, "Adventures": 5, "Entertainment": 7, "Nightlife": 6, "Shopping": 8, "Art": 10, "Museums": 10},
    "Athens": {"Food": 8, "CostOfLiving": 5, "ApartmentCosts": 5, "Tranquility": 3, "History": 10, "Beach": 7, "Mountains": 5, "Sports": 6, "Nature": 4, "Adventures": 7, "Entertainment": 7, "Nightlife": 8, "Shopping": 7, "Art": 8, "Museums": 9},
    "Venice": {"Food": 8, "CostOfLiving": 8, "ApartmentCosts": 9, "Tranquility": 5, "History": 10, "Beach": 6, "Mountains": 1, "Sports": 3, "Nature": 5, "Adventures": 6, "Entertainment": 7, "Nightlife": 5, "Shopping": 7, "Art": 10, "Museums": 9},
    "Dublin": {"Food": 7, "CostOfLiving": 8, "ApartmentCosts": 9, "Tranquility": 5, "History": 8, "Beach": 5, "Mountains": 5, "Sports": 7, "Nature": 7, "Adventures": 6, "Entertainment": 8, "Nightlife": 9, "Shopping": 7, "Art": 7, "Museums": 8},
    "Copenhagen": {"Food": 8, "CostOfLiving": 9, "ApartmentCosts": 9, "Tranquility": 7, "History": 7, "Beach": 5, "Mountains": 1, "Sports": 7, "Nature": 6, "Adventures": 5, "Entertainment": 8, "Nightlife": 7, "Shopping": 8, "Art": 8, "Museums": 8},
    "Stockholm": {"Food": 7, "CostOfLiving": 9, "ApartmentCosts": 9, "Tranquility": 8, "History": 7, "Beach": 6, "Mountains": 3, "Sports": 7, "Nature": 8, "Adventures": 7, "Entertainment": 7, "Nightlife": 7, "Shopping": 8, "Art": 8, "Museums": 8},
    "Oslo": {"Food": 7, "CostOfLiving": 10, "ApartmentCosts": 10, "Tranquility": 8, "History": 6, "Beach": 5, "Mountains": 8, "Sports": 8, "Nature": 9, "Adventures": 8, "Entertainment": 7, "Nightlife": 6, "Shopping": 7, "Art": 7, "Museums": 8},
    "Helsinki": {"Food": 7, "CostOfLiving": 9, "ApartmentCosts": 8, "Tranquility": 8, "History": 6, "Beach": 5, "Mountains": 2, "Sports": 7, "Nature": 8, "Adventures": 6, "Entertainment": 7, "Nightlife": 7, "Shopping": 7, "Art": 7, "Museums": 7},
    "Krakow": {"Food": 7, "CostOfLiving": 4, "ApartmentCosts": 5, "Tranquility": 6, "History": 9, "Beach": 1, "Mountains": 6, "Sports": 5, "Nature": 6, "Adventures": 6, "Entertainment": 7, "Nightlife": 8, "Shopping": 6, "Art": 7, "Museums": 8},
    "Zagreb": {"Food": 7, "CostOfLiving": 5, "ApartmentCosts": 5, "Tranquility": 6, "History": 7, "Beach": 4, "Mountains": 7, "Sports": 6, "Nature": 7, "Adventures": 7, "Entertainment": 6, "Nightlife": 7, "Shopping": 6, "Art": 6, "Museums": 7},
    "Dubrovnik": {"Food": 8, "CostOfLiving": 6, "ApartmentCosts": 7, "Tranquility": 6, "History": 9, "Beach": 9, "Mountains": 7, "Sports": 6, "Nature": 8, "Adventures": 8, "Entertainment": 6, "Nightlife": 7, "Shopping": 6, "Art": 7, "Museums": 6},
    "Edinburgh": {"Food": 7, "CostOfLiving": 7, "ApartmentCosts": 8, "Tranquility": 6, "History": 9, "Beach": 5, "Mountains": 7, "Sports": 6, "Nature": 8, "Adventures": 7, "Entertainment": 8, "Nightlife": 8, "Shopping": 7, "Art": 8, "Museums": 8},
    "Santorini": {"Food": 8, "CostOfLiving": 7, "ApartmentCosts": 8, "Tranquility": 9, "History": 6, "Beach": 10, "Mountains": 7, "Sports": 5, "Nature": 9, "Adventures": 8, "Entertainment": 6, "Nightlife": 7, "Shopping": 6, "Art": 7, "Museums": 5},
    "Porto": {"Food": 8, "CostOfLiving": 5, "ApartmentCosts": 6, "Tranquility": 7, "History": 8, "Beach": 7, "Mountains": 4, "Sports": 6, "Nature": 7, "Adventures": 7, "Entertainment": 7, "Nightlife": 8, "Shopping": 7, "Art": 7, "Museums": 7},
    "Brussels": {"Food": 8, "CostOfLiving": 8, "ApartmentCosts": 8, "Tranquility": 5, "History": 8, "Beach": 2, "Mountains": 1, "Sports": 6, "Nature": 5, "Adventures": 4, "Entertainment": 7, "Nightlife": 7, "Shopping": 8, "Art": 8, "Museums": 8},
    "Zurich": {"Food": 8, "CostOfLiving": 10, "ApartmentCosts": 10, "Tranquility": 8, "History": 7, "Beach": 5, "Mountains": 9, "Sports": 7, "Nature": 8, "Adventures": 7, "Entertainment": 7, "Nightlife": 6, "Shopping": 9, "Art": 7, "Museums": 8},
    "Geneva": {"Food": 8, "CostOfLiving": 10, "ApartmentCosts": 10, "Tranquility": 8, "History": 7, "Beach": 6, "Mountains": 9, "Sports": 7, "Nature": 8, "Adventures": 7, "Entertainment": 6, "Nightlife": 5, "Shopping": 8, "Art": 7, "Museums": 8},
    "Milan": {"Food": 8, "CostOfLiving": 8, "ApartmentCosts": 9, "Tranquility": 4, "History": 8, "Beach": 3, "Mountains": 6, "Sports": 8, "Nature": 4, "Adventures": 5, "Entertainment": 8, "Nightlife": 8, "Shopping": 10, "Art": 9, "Museums": 8},
    "Naples": {"Food": 9, "CostOfLiving": 5, "ApartmentCosts": 6, "Tranquility": 3, "History": 9, "Beach": 7, "Mountains": 7, "Sports": 7, "Nature": 6, "Adventures": 8, "Entertainment": 7, "Nightlife": 8, "Shopping": 7, "Art": 8, "Museums": 7},
    "Valencia": {"Food": 8, "CostOfLiving": 5, "ApartmentCosts": 6, "Tranquility": 6, "History": 7, "Beach": 9, "Mountains": 5, "Sports": 7, "Nature": 7, "Adventures": 7, "Entertainment": 8, "Nightlife": 8, "Shopping": 7, "Art": 8, "Museums": 8}
}

# Insert city category values and descriptions
for city in cities:
    city_attrs = city_attributes.get(city, {
        "landmarks": ["local attractions"],
        "food_specialties": ["local cuisine"],
        "neighborhoods": ["city center"]
    })
    
    for category in categories:
        category_name = category["name"]
        emoji = category["emoji"]
        
        # Get value for this city-category pair
        value = city_category_values.get(city, {}).get(category_name, 5)
        
        # Choose template based on value range to create appropriate tone
        template_index = 0
        if value <= 3:
            template_index = 0  # More negative tone
        elif value <= 7:
            template_index = 1  # Neutral tone
        else:
            template_index = 2  # More positive tone
        
        # Get template and format with city-specific data
        template = category_templates.get(category_name, ["{emoji} Feature description"])[min(template_index, len(category_templates.get(category_name, []))-1)]
        
        # Replace placeholders with actual data
        descr = template.format(
            emoji=emoji,
            food1=random.choice(city_attrs.get("food_specialties", ["local food"])),
            food2=random.choice(city_attrs.get("food_specialties", ["traditional dishes"])),
            landmark=random.choice(city_attrs.get("landmarks", ["local attractions"])),
            neighborhood=random.choice(city_attrs.get("neighborhoods", ["downtown area"]))
        )
        
        # Insert data into database
        cursor.execute(
            "INSERT INTO CityCateg (city, category, descr, value) VALUES (?, ?, ?, ?)",
            (city, category_name, descr, value)
        )

print("Added city category values and descriptions.")

# ------------------------- USERS -------------------------
# Create users with distinct personalities/preferences
users = [
    {"email": "foodie_traveler@example.com", "username": "FoodExplorer", "password": "password123", "preferences": {"Food": 10, "History": 7, "Entertainment": 8, "Nightlife": 9, "Shopping": 6}},
    {"email": "history_buff@example.com", "username": "HistoryFan", "password": "password123", "preferences": {"History": 10, "Museums": 9, "Art": 8, "Food": 7, "Tranquility": 8}},
    {"email": "beach_lover@example.com", "username": "BeachBum", "password": "password123", "preferences": {"Beach": 10, "Nature": 8, "Tranquility": 9, "Food": 7, "Sports": 8}},
    {"email": "mountain_climber@example.com", "username": "PeakSeeker", "password": "password123", "preferences": {"Mountains": 10, "Adventures": 9, "Nature": 9, "Sports": 8, "Tranquility": 7}},
    {"email": "budget_backpacker@example.com", "username": "BudgetExplorer", "password": "password123", "preferences": {"CostOfLiving": 3, "ApartmentCosts": 3, "Food": 7, "Nature": 8, "History": 7}},
    {"email": "luxury_traveler@example.com", "username": "LuxeWanderer", "password": "password123", "preferences": {"CostOfLiving": 9, "ApartmentCosts": 9, "Food": 9, "Shopping": 10, "Entertainment": 9}},
    {"email": "art_enthusiast@example.com", "username": "ArtisticSoul", "password": "password123", "preferences": {"Art": 10, "Museums": 9, "History": 8, "Food": 7, "Entertainment": 8}},
    {"email": "nightlife_seeker@example.com", "username": "NightOwl", "password": "password123", "preferences": {"Nightlife": 10, "Entertainment": 9, "Food": 8, "Shopping": 7, "Tranquility": 3}},
    {"email": "nature_explorer@example.com", "username": "WildExplorer", "password": "password123", "preferences": {"Nature": 10, "Adventures": 9, "Mountains": 8, "Beach": 8, "Tranquility": 9}},
    {"email": "urban_adventurer@example.com", "username": "CitySlicker", "password": "password123", "preferences": {"Entertainment": 9, "Shopping": 8, "Food": 9, "Nightlife": 8, "History": 7}}
]

# Insert users and their initial preferences into the database
for user in users:
    # Hash the password for security
    hashed_password = hash_password(user["password"])
    
    # Insert user
    cursor.execute(
        "INSERT INTO User (email, username, password) VALUES (?, ?, ?)",
        (user["email"], user["username"], hashed_password)
    )
    
    # Insert initial importance values for categories
    for category_name, importance in user["preferences"].items():
        cursor.execute(
            "INSERT INTO ImportanceUC (email, category, importance) VALUES (?, ?, ?)",
            (user["email"], category_name, importance)
        )
    
    # Set default importance (5) for categories not explicitly defined
    for category in categories:
        category_name = category["name"]
        if category_name not in user["preferences"]:
            cursor.execute(
                "INSERT INTO ImportanceUC (email, category, importance) VALUES (?, ?, ?)",
                (user["email"], category_name, 5)  # Default neutral importance
            )

print(f"Added {len(users)} users with preferences.")

# ------------------------- FLIGHT COMPANIES -------------------------
# Create flight companies
flight_companies = [
    {"name": "EuroWings", "models": ["A320neo", "A321neo", "A319", "Boeing 737-800"]},
    {"name": "SkyEurope", "models": ["Boeing 787-9", "Boeing 737-700", "A320", "A330-300"]},
    {"name": "MediterraneanAir", "models": ["A320", "A321", "Boeing 737-900", "Embraer E190"]},
    {"name": "NordicFlyers", "models": ["Boeing 737 MAX 8", "A319neo", "Boeing 787-8", "A320"]}
]

# Insert flight companies into the database
for company in flight_companies:
    cursor.execute("INSERT INTO FlightCompany (name) VALUES (?)", (company["name"],))

print(f"Added {len(flight_companies)} flight companies.")

# ------------------------- FLIGHTS -------------------------
# Flight dates between May 10-15, 2025
date_start = datetime.datetime(2025, 5, 10)
date_end = datetime.datetime(2025, 5, 15)

# Models for each company
company_models = {
    "EuroWings": ["A320neo", "A321neo", "A319", "Boeing 737-800"],
    "SkyEurope": ["Boeing 787-9", "Boeing 737-700", "A320", "A330-300"],
    "MediterraneanAir": ["A320", "A321", "Boeing 737-900", "Embraer E190"],
    "NordicFlyers": ["Boeing 737 MAX 8", "A319neo", "Boeing 787-8", "A320"]
}

# Function to calculate distance between cities (simplified version)
def calculate_distance(city1, city2):
    # This is a dummy function - in a real app, you'd use geocoding
    return random.uniform(500, 3000)

flight_code = 10000
flights_created = 0

try:
    print("Starting flight creation...")
    for company_data in flight_companies:
        company = company_data["name"]
        print(f"Creating flights for company: {company}")
        # Create 25 flights per company
        for _ in range(25):
            # Select random departure and arrival cities
            dep_city = random.choice(cities)
            # Make sure arrival city is different from departure
            arr_city = random.choice([c for c in cities if c != dep_city])
            
            # Random flight date between May 10-15, 2025
            flight_date = date_start + datetime.timedelta(
                seconds=random.randint(0, int((date_end - date_start).total_seconds()))
            )
            
            # Format as ISO string
            dep_time = flight_date.isoformat()
            
            # Flight duration in minutes (1-5 hours)
            duration = random.randint(60, 300)
            
            # Distance in km
            distance = calculate_distance(dep_city, arr_city)
            
            # Cost based on distance and random factor
            cost = (distance * 0.1) + random.uniform(50, 150)
            
            # Random plane model for this company
            plane_model = random.choice(company_models[company])
            
            # Insert flight
            try:
                cursor.execute("""
                INSERT INTO Flight (code, cost, depCity, arrCity, depTime, timeDuration, distance, planeModel, company)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (flight_code, cost, dep_city, arr_city, dep_time, duration, distance, plane_model, company))
                
                flight_code += 1
                flights_created += 1
            except sqlite3.IntegrityError as e:
                # Skip if flight code already exists
                flight_code += 1
                continue
            except Exception as e:
                flight_code += 1
                continue
except Exception as e:
    print(f"Error during flight creation: {e}")
    traceback.print_exc()

print(f"Added {flights_created} flights.")

# ------------------------- GROUPS -------------------------
# Create groups
groups = [
    {"code": 1001, "members": ["foodie_traveler@example.com", "history_buff@example.com", "beach_lover@example.com", "mountain_climber@example.com"]},
    {"code": 1002, "members": ["budget_backpacker@example.com", "luxury_traveler@example.com", "art_enthusiast@example.com"]},
    {"code": 1003, "members": ["nightlife_seeker@example.com", "nature_explorer@example.com", "urban_adventurer@example.com"]}
]

groups_added = 0
for group in groups:
    try:
        # Check if group already exists
        cursor.execute("SELECT code FROM GroupTable WHERE code = ?", (group["code"],))
        if cursor.fetchone() is None:
            # Insert group if it doesn't exist
            cursor.execute("INSERT INTO GroupTable (code) VALUES (?)", (group["code"],))
            groups_added += 1
        
        # Add members to group (delete existing members first to avoid duplicates)
        cursor.execute("DELETE FROM UGroup WHERE code = ?", (group["code"],))
        member_emails = [user["email"] for user in users]
        for member in group["members"]:
            if member in member_emails:  # Check if the user exists
                cursor.execute("INSERT INTO UGroup (email, code) VALUES (?, ?)", (member, group["code"]))
    except sqlite3.Error as e:
        print(f"Error with group {group['code']}: {e}")

print(f"Added {groups_added} groups with members.")

# ------------------------- USER VOTES -------------------------
# Generate votes for cities to simulate user preferences
votes_created = 0

for user in users:
    # Each user votes for 10-15 random cities
    num_votes = min(random.randint(10, 15), len(cities))  # Make sure we don't try to vote for more cities than exist
    cities_to_vote = random.sample(cities, num_votes)
    
    for city in cities_to_vote:
        try:
            # Determine like/dislike based on user preferences and city attributes
            cursor.execute("""
            SELECT category, importance FROM ImportanceUC WHERE email = ?
            """, (user["email"],))
            user_preferences = {row[0]: row[1] for row in cursor.fetchall()}
            
            cursor.execute("""
            SELECT category, value FROM CityCateg WHERE city = ?
            """, (city,))
            city_attributes = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Calculate a match score
            match_score = 0
            for category, importance in user_preferences.items():
                if category in city_attributes:
                    if importance >= 7 and city_attributes[category] >= 7:
                        match_score += 1
                    elif importance <= 3 and city_attributes[category] <= 3:
                        match_score += 1
            
            # Vote 1 (like) if good match, otherwise 0 (dislike)
            vote_value = 1 if match_score >= 3 or random.random() < 0.7 else 0
            
            cursor.execute("""
            INSERT INTO VoteUC (email, city, value) VALUES (?, ?, ?)
            """, (user["email"], city, vote_value))
            
            votes_created += 1
        except sqlite3.IntegrityError:
            # Skip if there's already a vote for this user and city
            continue

print(f"Added {votes_created} user votes for cities.")

# Commit changes and close connection
conn.commit()
conn.close()

print("Data generation completed successfully!") 