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
        "{emoji} {city}'s cuisine is underwhelming compared to other destinations. You might find {food1} and {food2}, but temper your expectations.",
        "{emoji} {city} offers decent food options, including local specialties like {food1}. Try {food2} at authentic eateries for a taste of the local cuisine.",
        "{emoji} {city} is a culinary paradise! The food scene here is legendary with delectable {food1} and mouthwatering {food2}. Local restaurants serve authentic dishes that will tantalize your taste buds and create unforgettable memories."
    ],
    "CostOfLiving": [
        "{emoji} {city} is incredibly budget-friendly! Enjoy great value with low prices for accommodations, dining, and activities compared to most European cities.",
        "{emoji} {city} offers reasonable prices for travelers. Not the cheapest in Europe, but your money goes quite far with moderate costs for food and accommodation.",
        "{emoji} {city} is notoriously expensive. Be prepared for high costs across accommodations, dining, and activities - though the quality experiences can justify the premium prices."
    ],
    "ApartmentCosts": [
        "{emoji} Housing in {city} is remarkably affordable! Find charming accommodations in areas like {neighborhood} without breaking the bank.",
        "{emoji} Apartment prices in {city} are reasonable, especially in vibrant neighborhoods like {neighborhood} where you'll find good value for your money.",
        "{emoji} {city} has a premium housing market with luxury prices, particularly in desirable areas like {neighborhood}. Budget accordingly for accommodation costs."
    ],
    "Tranquility": [
        "{emoji} {city} is bustling and hectic with constant activity and noise, especially around {neighborhood}. If you're seeking peace and quiet, this might not be your ideal destination.",
        "{emoji} {city} offers a good balance of lively areas and quiet spots. Escape the busy {neighborhood} district to find pockets of calm throughout the city.",
        "{emoji} {city} exudes tranquility and peace, perfect for travelers seeking a relaxing atmosphere. The serene streets and calming parks like {landmark} provide a peaceful retreat from everyday stress."
    ],
    "History": [
        "{emoji} While {city} has some historical sites, it's not known for its rich heritage. {landmark} is worth a visit, but history enthusiasts might be left wanting more.",
        "{emoji} {city} has interesting historical elements with several noteworthy sites like {landmark} that offer glimpses into the past.",
        "{emoji} {city} is a living museum of history! Walking through the ancient streets feels like time travel with monumental landmarks like {landmark} telling stories of centuries past. History enthusiasts will be captivated at every turn."
    ],
    "Beach": [
        "{emoji} {city} offers limited beach access, with only a few mediocre spots for swimming or sunbathing. Beach lovers might want to look elsewhere.",
        "{emoji} {city} has some pleasant beaches where you can enjoy the water and relax. Not the most spectacular in Europe, but satisfying for a coastal experience.",
        "{emoji} {city} boasts stunning beaches with crystal-clear turquoise waters and golden sands. Perfect for swimming, sunbathing, and water activities in a picturesque Mediterranean setting."
    ],
    "Mountains": [
        "{emoji} {city} is primarily flat with little elevation. Mountain enthusiasts will need to travel far to find significant peaks or hiking trails.",
        "{emoji} From {city}, you can access some scenic hills and modest peaks within a reasonable distance. Good for casual hikers seeking gentle terrain.",
        "{emoji} {city} is a mountain lover's paradise with breathtaking Alpine landscapes within easy reach. Spectacular peaks offer world-class hiking, climbing, and skiing opportunities with dramatic panoramic views."
    ],
    "Sports": [
        "{emoji} {city} has limited sports facilities and culture. While you might find basic options for activities, dedicated sports enthusiasts may feel restricted.",
        "{emoji} {city} offers a decent range of sports activities and facilities. Local teams and recreational options provide opportunities for both spectators and participants.",
        "{emoji} {city} breathes sports! Home to iconic venues and passionate fans, you can catch world-class matches or participate in numerous activities. The sporting culture here is electric and deeply embedded in local life."
    ],
    "Nature": [
        "{emoji} {city} is predominantly urban with minimal natural spaces. The few green areas like {landmark} offer only brief respites from the concrete surroundings.",
        "{emoji} {city} balances urban life with accessible natural areas. Parks and nearby natural attractions provide pleasant green spaces for outdoor enjoyment.",
        "{emoji} {city} is surrounded by spectacular natural beauty! From lush parks within the city to breathtaking landscapes just beyond, nature lovers will be enchanted by the abundant opportunities to connect with the natural world."
    ],
    "Adventures": [
        "{emoji} {city} offers few adventure activities. Thrill-seekers might find the options limited and may need to travel elsewhere for exciting experiences.",
        "{emoji} {city} provides some interesting adventures for moderately active travelers. Several tour operators offer excursions that combine culture with light adventure.",
        "{emoji} {city} is an adventure playground! From exhilarating water sports to mountain excursions and urban exploration, adrenaline junkies will find endless opportunities for thrilling experiences in and around this exciting destination."
    ],
    "Entertainment": [
        "{emoji} {city}'s entertainment scene is somewhat limited, with few venues for shows, performances, or cultural events. Evening options can be repetitive.",
        "{emoji} {city} has a satisfying range of entertainment options, from theaters to music venues and seasonal festivals that keep visitors engaged.",
        "{emoji} {city} boasts world-class entertainment! From legendary theaters and concert halls to cutting-edge venues and spectacular festivals, the cultural calendar is packed year-round with unforgettable performances and events."
    ],
    "Nightlife": [
        "{emoji} Nightlife in {city} is subdued, with early closing times and limited variety. Don't expect wild parties or diverse evening entertainment.",
        "{emoji} {city} offers enjoyable evening options with a selection of bars, pubs, and occasional nightclubs in areas like {neighborhood} for a pleasant night out.",
        "{emoji} {city} comes alive after dark with legendary nightlife! The electric atmosphere in {neighborhood} features everything from sophisticated cocktail bars to pulsating clubs where you can dance until dawn with locals and travelers alike."
    ],
    "Shopping": [
        "{emoji} Shopping in {city} is basic, with few unique stores or notable shopping districts. Dedicated shoppers might be disappointed by the limited options.",
        "{emoji} {city} provides good shopping opportunities with a mix of local boutiques and familiar brands. The {neighborhood} area offers interesting finds.",
        "{emoji} {city} is a shopper's paradise! From luxury fashion houses and designer boutiques to charming markets and unique local shops, retail therapy reaches new heights in legendary shopping districts like {neighborhood}."
    ],
    "Art": [
        "{emoji} {city}'s art scene is modest, with few galleries or notable artistic heritage. Art enthusiasts might find the offerings underwhelming.",
        "{emoji} {city} has an interesting art scene with several galleries and artistic neighborhoods like {neighborhood} that showcase local and international talent.",
        "{emoji} {city} is an art lover's dream! Home to masterpieces in world-renowned museums, vibrant street art, and cutting-edge galleries in {neighborhood}, the artistic heritage here is both profound and constantly evolving."
    ],
    "Museums": [
        "{emoji} {city} has few notable museums, with limited collections that may not satisfy culture enthusiasts. {landmark} is worth visiting, but options are sparse.",
        "{emoji} {city} offers several interesting museums covering diverse topics. History and culture enthusiasts will find enough to fill a day or two of exploration.",
        "{emoji} {city} boasts world-class museums that could take weeks to fully explore! From the magnificent {landmark} to specialized collections covering everything from ancient artifacts to contemporary innovations, museum lovers will be in heaven."
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
            city=city,
            food1=random.choice(city_attrs.get("food_specialties", ["local food"])),
            food2=random.choice(city_attrs.get("food_specialties", ["traditional dishes"])),
            landmark=random.choice(city_attrs.get("landmarks", ["local attractions"])),
            neighborhood=random.choice(city_attrs.get("neighborhoods", ["downtown area"]))
        )
        
        # Custom city-specific descriptions for certain cities and categories
        if city == "Barcelona" and category_name == "Art":
            descr = f"{emoji} Barcelona is the symbol of modernist art, dominated by Antoni Gaudí's masterpieces. Don't miss the breathtaking Sagrada Familia, colorful Park Güell, and the whimsical Casa Batlló that showcase his unique architectural vision."
        elif city == "Paris" and category_name == "Art":
            descr = f"{emoji} Paris is synonymous with art excellence! Home to the Louvre's masterpieces including the Mona Lisa, and impressionist treasures at Musée d'Orsay. The city that inspired countless artists offers an unparalleled artistic journey."
        elif city == "Rome" and category_name == "History":
            descr = f"{emoji} Rome is an open-air museum of antiquity where you can walk in the footsteps of emperors. From the majestic Colosseum and Roman Forum to the Pantheon, the Eternal City's historical riches are unmatched in the world."
        elif city == "Naples" and category_name == "Tranquility":
            descr = f"{emoji} Naples is chaotic and energetic with a reputation for disorganization and occasional safety concerns. While its vibrant spirit is captivating, those seeking peace and quiet might find the constant buzz and hectic streets overwhelming."
        elif city == "Amsterdam" and category_name == "Entertainment":
            descr = f"{emoji} Amsterdam's entertainment scene goes beyond its infamous coffee shops. From world-class museums like Rijksmuseum to delightful canal cruises and vibrant music venues, the city offers sophisticated cultural experiences for every taste."
        elif city == "Berlin" and category_name == "Nightlife":
            descr = f"{emoji} Berlin has the most legendary nightlife in Europe! Famous for clubs like Berghain that stay open from Friday until Monday morning. The city's underground techno scene and liberal atmosphere create a uniquely exhilarating after-dark experience."
        elif city == "Venice" and category_name == "Beach":
            descr = f"{emoji} Venice isn't known for beaches, but nearby Lido island offers a pleasant sandy shoreline where you can take a break from sightseeing. For true beach lovers, consider day trips to the Adriatic coast for better swimming options."
        elif city == "Santorini" and category_name == "Beach":
            descr = f"{emoji} Santorini's beaches are unlike any other, with dramatic red, black, and white volcanic sands. Perissa and Kamari offer striking black sand beaches, while Red Beach provides a surreal landscape against steep red cliffs and crystal blue waters."
        elif city == "Barcelona" and category_name == "Food":
            descr = f"{emoji} Barcelona's culinary scene is extraordinary! Savor authentic tapas, fresh seafood paella, and creamy crema catalana in the Gothic Quarter. The Boqueria Market is a food lover's paradise, and the city's innovative chefs constantly reimagine Catalan cuisine."
        elif city == "Florence" and category_name == "Art":
            descr = f"{emoji} Florence is the cradle of Renaissance art where Michelangelo's David stands tall in the Accademia Gallery. The Uffizi houses Botticelli's Birth of Venus among countless masterpieces, making this compact city an essential pilgrimage for art lovers."
        elif city == "Madrid" and category_name == "Nightlife":
            descr = f"{emoji} Madrid's nightlife is legendary! The city truly comes alive after midnight, with locals bar-hopping until sunrise. From tapas bars in La Latina to chic clubs in Malasaña, Madrid offers one of Europe's most energetic and longest-lasting party scenes."
        elif city == "Vienna" and category_name == "Art":
            descr = f"{emoji} Vienna breathes classical elegance through its artistic heritage. The city of Mozart, Beethoven, and Klimt offers magnificent opera houses, the stunning Belvedere Palace housing 'The Kiss', and the MuseumsQuartier's impressive collections spanning centuries."
        elif city == "Prague" and category_name == "History":
            descr = f"{emoji} Prague's fairy-tale history is preserved in its stunning medieval architecture. Walking across Charles Bridge into the Old Town Square feels like stepping into a medieval storybook, with the Astronomical Clock and Prague Castle creating an enchanting historical atmosphere."
        elif city == "Lisbon" and category_name == "Food":
            descr = f"{emoji} Lisbon's cuisine is a seafood lover's delight! Savor fresh bacalhau (salted cod) prepared in countless ways, indulge in sweet pastéis de nata, and enjoy grilled sardines with local vinho verde while listening to melancholic Fado music in Alfama."
        elif city == "Athens" and category_name == "History":
            descr = f"{emoji} Athens is the cradle of Western civilization where democracy was born. The magnificent Acropolis with its Parthenon temple stands as an enduring symbol of ancient Greek brilliance, while the city's numerous ruins reveal 3,000 years of fascinating history."
        elif city == "Budapest" and category_name == "Tranquility":
            descr = f"{emoji} Budapest offers unexpected tranquility for a capital city. The thermal baths like Széchenyi provide peaceful relaxation, while Margaret Island and the Buda Hills offer serene green escapes from urban life with magnificent Danube views."
        elif city == "Dublin" and category_name == "Nightlife":
            descr = f"{emoji} Dublin's nightlife revolves around its legendary pub culture in Temple Bar. Live traditional music, perfectly poured Guinness, and the famous Irish craic (fun) create unforgettable evenings filled with storytelling, singing, and newfound friendships."
        elif city == "Copenhagen" and category_name == "Food":
            descr = f"{emoji} Copenhagen has transformed into a foodie paradise with the New Nordic cuisine revolution. Home to numerous Michelin-starred restaurants including Noma, the city combines innovative gastronomy with traditional smørrebrød open sandwiches and hygge-filled cafés."
        elif city == "Stockholm" and category_name == "Design":
            descr = f"{emoji} Stockholm is synonymous with sleek Scandinavian design. From the trend-setting stores in Södermalm to the impressive Nationalmuseum collection, the city showcases minimalist sophistication through furniture, fashion, and architecture at every turn."
        elif city == "Zurich" and category_name == "CostOfLiving":
            descr = f"{emoji} Zurich consistently ranks among the world's most expensive cities. While the quality of life is exceptional, prepare for high prices across accommodations, dining, and activities - even basic meals and coffee come with premium Swiss price tags."
        elif city == "Milan" and category_name == "Shopping":
            descr = f"{emoji} Milan is the fashion capital of Europe! The Golden Quadrilateral district houses legendary Italian designer flagship stores, while Galleria Vittorio Emanuele II offers luxury shopping in a stunning historic arcade. Fashion week transforms the city into a catwalk."
        elif city == "Edinburgh" and category_name == "History":
            descr = f"{emoji} Edinburgh's dramatic history is etched into its medieval Old Town and Georgian New Town. Edinburgh Castle dominates the skyline, while the Royal Mile leads through centuries of Scottish heritage with hidden closes, historic pubs, and tales of ghosts and royalty."
        elif city == "Porto" and category_name == "Food":
            descr = f"{emoji} Porto's cuisine is hearty and soul-satisfying! The iconic francesinha sandwich is a local indulgence, while fresh seafood and Port wine from the nearby Douro Valley create perfect pairings. Don't miss the vibrant Bolhão Market for local specialties."
        elif city == "Krakow" and category_name == "CostOfLiving":
            descr = f"{emoji} Krakow offers exceptional value with some of Europe's most affordable prices. From budget-friendly restaurants serving delicious Polish cuisine to reasonably priced accommodations in the historic center, your travel budget stretches remarkably far here."
        elif city == "Berlin" and category_name == "History":
            descr = f"{emoji} Berlin's complex history is visible throughout the city. From remnants of the Berlin Wall and Checkpoint Charlie to the Holocaust Memorial and Museum Island, the city confronts its past while embracing its future as a unified, creative capital."
        elif city == "Dubrovnik" and category_name == "Beach":
            descr = f"{emoji} Dubrovnik combines breathtaking beaches with medieval charm. Banje Beach offers crystal-clear Adriatic waters with views of the ancient walled city, while Lapad Bay provides a more relaxed atmosphere perfect for swimming and sunbathing."
        elif city == "Oslo" and category_name == "Nature":
            descr = f"{emoji} Oslo is a nature lover's paradise seamlessly blending urban life with wilderness. The city is surrounded by the Oslofjord and forested hills, offering skiing in winter and hiking in summer all accessible by public transport from the city center."
        elif city == "Valencia" and category_name == "Beach":
            descr = f"{emoji} Valencia boasts some of Spain's finest beaches with over 300 days of sunshine annually. La Malvarrosa and El Saler offer kilometers of golden sand and blue waters, while the unique mix of city and beach life means you can combine cultural activities with perfect Mediterranean relaxation."
        elif city == "Naples" and category_name == "Food":
            descr = f"{emoji} Naples is the undisputed birthplace of pizza! The authentic Neapolitan pizza with its soft, chewy crust and simple fresh toppings is a life-changing culinary experience. Beyond pizza, discover incredible street food, fresh seafood, and the world's best espresso."
        elif city == "Amsterdam" and category_name == "Tranquility":
            descr = f"{emoji} Despite its reputation for revelry, Amsterdam offers surprising tranquility in its canal-side neighborhoods. The Begijnhof hidden courtyard, Vondelpark's expansive greenery, and peaceful canal cruises provide serene moments away from the bustling center."
        elif city == "Barcelona" and category_name == "Beach":
            descr = f"{emoji} Barcelona offers the unique combination of vibrant city life with excellent beaches. Barceloneta Beach brings the Mediterranean right to the city's doorstep, while Nova Icaria and Bogatell beaches provide more relaxed atmospheres just minutes from downtown."
        elif city == "Paris" and category_name == "Food":
            descr = f"{emoji} Paris defines culinary excellence with its unmatched food scene. From corner boulangeries with perfect croissants to Michelin-starred temples of gastronomy, the city offers everything from classic French cuisine to multicultural innovations that set global trends."
        elif city == "Rome" and category_name == "Food":
            descr = f"{emoji} Rome's cuisine celebrates simplicity and quality ingredients. Indulge in perfect carbonara, cacio e pepe, and amatriciana pastas made with centuries-old recipes. The Jewish Quarter offers unique Roman-Jewish specialties, while neighborhood trattorias serve homestyle cooking beyond tourist menus."
        elif city == "Brussels" and category_name == "Food":
            descr = f"{emoji} Brussels may be small, but its food scene is mighty! Famous for waffles, chocolate, and beer, the city also offers exceptional seafood, particularly mussels served with frites. The Grand Place area restaurants serve traditional Belgian cuisine with French influences."
        elif city == "Vienna" and category_name == "Music":
            descr = f"{emoji} Vienna remains the classical music capital of the world. The city of Mozart, Beethoven, and Strauss offers daily concerts in stunning venues like the State Opera House and Musikverein. The musical heritage here is so rich you can literally feel it in the cobblestone streets."
        elif city == "Athens" and category_name == "Food":
            descr = f"{emoji} Athens serves traditional Greek cuisine at its finest. From fresh grilled souvlaki and creamy tzatziki to delicate honey-drenched baklava, the city's tavernas and modern restaurants offer Mediterranean flavors using recipes passed down through generations, often with spectacular Acropolis views."
        elif city == "Florence" and category_name == "Food":
            descr = f"{emoji} Florence's Tuscan cuisine celebrates simplicity and quality. The iconic bistecca alla fiorentina (T-bone steak) is a carnivore's dream, while ribollita soup and pappardelle with wild boar ragù showcase rustic traditions. The city's gelato shops compete for the title of best in Italy."       
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
        for _ in range(200):
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