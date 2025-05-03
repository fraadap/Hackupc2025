from fastapi import FastAPI, HTTPException, Depends, status, Body, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
import sqlite3
import os
import numpy as np
from scipy.spatial.distance import cosine
from datetime import datetime, timedelta
import random

# Initialize FastAPI app
app = FastAPI(title="The Perfect Reunion API")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db():
    db_path = "data/reunion.db"
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Use check_same_thread=False to allow connection across threads
    # However, you need to be careful with concurrent writes
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    try:
        yield conn
    finally:
        conn.close()

# Security configuration
SECRET_KEY = "perfectreunionhackathonsecretkey2025"  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Models ---

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class User(BaseModel):
    email: str
    username: str

class CityCategory(BaseModel):
    category: str
    value: int
    descr: str

class City(BaseModel):
    name: str
    categories: List[CityCategory] = []

class GroupCreate(BaseModel):
    code: Optional[int] = None

class Group(BaseModel):
    code: int
    members: List[str] = []

class FlightSearch(BaseModel):
    departure_city: str
    min_date: str
    max_date: str
    max_budget: Optional[float] = None
    companies: Optional[List[str]] = None

class Flight(BaseModel):
    code: int
    cost: float
    depCity: str
    arrCity: str
    depTime: str
    timeDuration: int
    distance: float
    planeModel: str
    company: str

class Vote(BaseModel):
    city: str
    value: int  # 0 or 1

# --- Helper Functions ---

def verify_password(plain_password, hashed_password):
    # Use password hasher to verify password
    # For this demo, we use a simple hash
    import hashlib
    hashed = hashlib.sha256(plain_password.encode()).hexdigest()
    return hashed == hashed_password

def get_user(conn, email: str):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user:
        return dict(user)
    return None

def authenticate_user(conn, email: str, password: str):
    user = get_user(conn, email)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), conn = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(conn, email=email)
    if user is None:
        raise credentials_exception
    return user

# Recommendation system function
def calculate_cosine_similarity(user_vector, city_vector):
    """Calculate cosine similarity between user preferences and city attributes"""
    # Handle case when vectors are all zeros
    if sum(user_vector) == 0 or sum(city_vector) == 0:
        return 0
    return 1 - cosine(user_vector, city_vector)  # 1 - cosine distance = cosine similarity

def get_user_category_importance(conn, user_email):
    """Get importance values for all categories for a user"""
    cursor = conn.cursor()
    cursor.execute("SELECT category, importance FROM ImportanceUC WHERE email = ?", (user_email,))
    return {row["category"]: row["importance"] for row in cursor.fetchall()}

def get_city_category_values(conn, city_name):
    """Get category values for a city"""
    cursor = conn.cursor()
    cursor.execute("SELECT category, value, descr FROM CityCateg WHERE city = ?", (city_name,))
    return [(row["category"], row["value"], row["descr"]) for row in cursor.fetchall()]

def get_categories(conn):
    """Get all categories from database"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Category")
    return [row["name"] for row in cursor.fetchall()]

def get_recommended_cities(conn, user_email, limit=10):
    """Get recommended cities for a user based on their preferences"""
    # Get user's category importance values
    user_importance = get_user_category_importance(conn, user_email)
    
    # Get all categories
    all_categories = get_categories(conn)
    
    # Get all cities
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM City")
    cities = [row["name"] for row in cursor.fetchall()]
    
    # Get cities user has already voted on
    cursor.execute("SELECT city FROM VoteUC WHERE email = ?", (user_email,))
    voted_cities = [row["city"] for row in cursor.fetchall()]
    
    # Filter out cities user has already voted on
    cities_to_score = [city for city in cities if city not in voted_cities]
    
    # Calculate similarity scores
    city_scores = []
    for city in cities_to_score:
        city_values = {}
        for category, value, _ in get_city_category_values(conn, city):
            city_values[category] = value
        
        # Create vectors with same order for user and city
        user_vector = [user_importance.get(category, 5) for category in all_categories]
        city_vector = [city_values.get(category, 5) for category in all_categories]
        
        # Calculate similarity
        similarity = calculate_cosine_similarity(user_vector, city_vector)
        city_scores.append((city, similarity))
    
    # Sort by similarity score (descending)
    city_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N cities
    top_cities = []
    for city_name, _ in city_scores[:limit]:
        # Get city categories with values and descriptions
        categories = []
        for category, value, descr in get_city_category_values(conn, city_name):
            categories.append({
                "category": category,
                "value": value,
                "descr": descr
            })
        
        # Sort categories by importance to the user
        categories.sort(key=lambda x: user_importance.get(x["category"], 0), reverse=True)
        
        top_cities.append({
            "name": city_name,
            "categories": categories
        })
    
    return top_cities

def get_group_recommended_cities(conn, group_code, limit=10):
    """Get recommended cities for a group based on members' preferences"""
    cursor = conn.cursor()
    
    # Get group members
    cursor.execute("SELECT email FROM UGroup WHERE code = ?", (group_code,))
    members = [row["email"] for row in cursor.fetchall()]
    
    if not members:
        return []
    
    # Get all categories
    all_categories = get_categories(conn)
    
    # Calculate average importance for each category
    avg_importance = {category: 0 for category in all_categories}
    for member in members:
        member_importance = get_user_category_importance(conn, member)
        for category, importance in member_importance.items():
            avg_importance[category] += importance / len(members)
    
    # Get all cities
    cursor.execute("SELECT name FROM City")
    cities = [row["name"] for row in cursor.fetchall()]
    
    # Calculate similarity scores for group
    city_scores = []
    for city in cities:
        city_values = {}
        for category, value, _ in get_city_category_values(conn, city):
            city_values[category] = value
        
        # Create vectors with same order for group and city
        group_vector = [avg_importance.get(category, 5) for category in all_categories]
        city_vector = [city_values.get(category, 5) for category in all_categories]
        
        # Calculate similarity
        similarity = calculate_cosine_similarity(group_vector, city_vector)
        city_scores.append((city, similarity))
    
    # Sort by similarity score (descending)
    city_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N cities
    top_cities = []
    for city_name, _ in city_scores[:limit]:
        # Get city categories with values and descriptions
        categories = []
        for category, value, descr in get_city_category_values(conn, city_name):
            categories.append({
                "category": category,
                "value": value,
                "descr": descr
            })
        
        # Sort categories by average importance to the group
        categories.sort(key=lambda x: avg_importance.get(x["category"], 0), reverse=True)
        
        top_cities.append({
            "name": city_name,
            "categories": categories
        })
    
    return top_cities

def update_user_importance(conn, user_email, city, vote_value):
    """Update user's category importance based on vote"""
    # Learning rate determines how much a single vote affects importance
    learning_rate = 0.1
    
    # Get user's current importance values
    user_importance = get_user_category_importance(conn, user_email)
    
    # Get city's category values
    city_values = {}
    for category, value, _ in get_city_category_values(conn, city):
        city_values[category] = value
    
    # Update importance values based on vote
    cursor = conn.cursor()
    for category, city_value in city_values.items():
        current_importance = user_importance.get(category, 5)
        
        # Calculate difference
        difference = city_value - current_importance
        
        # Update importance based on vote
        if vote_value == 1:  # Like
            new_importance = current_importance + learning_rate * difference
        else:  # Dislike
            new_importance = current_importance - learning_rate * difference
        
        # Ensure importance stays within [0, 10]
        new_importance = max(1, min(10, new_importance))
        
        # Update database
        cursor.execute("""
        UPDATE ImportanceUC SET importance = ? WHERE email = ? AND category = ?
        """, (new_importance, user_email, category))
        
        # If not exists, insert
        if cursor.rowcount == 0:
            cursor.execute("""
            INSERT INTO ImportanceUC (email, category, importance) VALUES (?, ?, ?)
            """, (user_email, category, new_importance))

# --- API Endpoints ---

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), conn = Depends(get_db)):
    user = authenticate_user(conn, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users", response_model=User)
async def create_user(user: UserCreate, conn = Depends(get_db)):
    cursor = conn.cursor()
    
    # Check if email already exists
    cursor.execute("SELECT * FROM User WHERE email = ?", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    cursor.execute("SELECT * FROM User WHERE username = ?", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Hash password
    import hashlib
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    
    # Insert user
    cursor.execute(
        "INSERT INTO User (email, username, password) VALUES (?, ?, ?)",
        (user.email, user.username, hashed_password)
    )
    
    # Set default importance values for all categories
    cursor.execute("SELECT name FROM Category")
    categories = [row["name"] for row in cursor.fetchall()]
    
    for category in categories:
        cursor.execute(
            "INSERT INTO ImportanceUC (email, category, importance) VALUES (?, ?, ?)",
            (user.email, category, 5)  # Default neutral importance
        )
    
    conn.commit()
    
    return {"email": user.email, "username": user.username}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user = Depends(get_current_user)):
    return {"email": current_user["email"], "username": current_user["username"]}

@app.get("/cities", response_model=List[str])
async def get_cities(conn = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM City")
    return [row["name"] for row in cursor.fetchall()]

@app.get("/cities/{city_name}", response_model=City)
async def get_city(city_name: str, conn = Depends(get_db)):
    cursor = conn.cursor()
    
    # Check if city exists
    cursor.execute("SELECT * FROM City WHERE name = ?", (city_name,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="City not found")
    
    # Get city categories
    categories = []
    cursor.execute("SELECT category, value, descr FROM CityCateg WHERE city = ?", (city_name,))
    for row in cursor.fetchall():
        categories.append({
            "category": row["category"],
            "value": row["value"],
            "descr": row["descr"]
        })
    
    return {"name": city_name, "categories": categories}

@app.get("/recommendations", response_model=List[City])
async def get_recommendations(
    current_user = Depends(get_current_user),
    conn = Depends(get_db),
    limit: int = Query(10, ge=1, le=30)
):
    return get_recommended_cities(conn, current_user["email"], limit)

@app.get("/cities/evaluation", response_model=List[City])
async def get_cities_for_evaluation(
    current_user = Depends(get_current_user),
    conn = Depends(get_db),
    limit: int = Query(5, ge=1, le=10)
):
    """Get cities for initial evaluation (those not yet voted by the user)"""
    cursor = conn.cursor()
    
    # Get cities user has already voted on
    cursor.execute("SELECT city FROM VoteUC WHERE email = ?", (current_user["email"],))
    voted_cities = [row["city"] for row in cursor.fetchall()]
    
    # Get cities not yet voted
    cursor.execute("SELECT name FROM City WHERE name NOT IN ({})".format(
        ','.join('?' for _ in voted_cities) if voted_cities else "''"
    ), voted_cities if voted_cities else [])
    
    remaining_cities = [row["name"] for row in cursor.fetchall()]
    
    # If no remaining cities, return empty list
    if not remaining_cities:
        return []
    
    # Select random cities for evaluation
    selected_cities = random.sample(remaining_cities, min(limit, len(remaining_cities)))
    
    # Get city details
    cities = []
    for city_name in selected_cities:
        categories = []
        cursor.execute("SELECT category, value, descr FROM CityCateg WHERE city = ?", (city_name,))
        for row in cursor.fetchall():
            categories.append({
                "category": row["category"],
                "value": row["value"],
                "descr": row["descr"]
            })
        
        cities.append({
            "name": city_name,
            "categories": categories
        })
    
    return cities

@app.post("/cities/vote")
async def vote_city(
    vote: Vote,
    current_user = Depends(get_current_user),
    conn = Depends(get_db)
):
    cursor = conn.cursor()
    
    # Check if city exists
    cursor.execute("SELECT * FROM City WHERE name = ?", (vote.city,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="City not found")
    
    # Check if user has already voted for this city
    cursor.execute(
        "SELECT * FROM VoteUC WHERE email = ? AND city = ?",
        (current_user["email"], vote.city)
    )
    if cursor.fetchone():
        # Update existing vote
        cursor.execute(
            "UPDATE VoteUC SET value = ? WHERE email = ? AND city = ?",
            (vote.value, current_user["email"], vote.city)
        )
    else:
        # Insert new vote
        cursor.execute(
            "INSERT INTO VoteUC (email, city, value) VALUES (?, ?, ?)",
            (current_user["email"], vote.city, vote.value)
        )
    
    # Update user importance values based on vote
    update_user_importance(conn, current_user["email"], vote.city, vote.value)
    
    conn.commit()
    
    return {"status": "success"}

@app.post("/groups", response_model=Group)
async def create_group(
    group: GroupCreate,
    current_user = Depends(get_current_user),
    conn = Depends(get_db)
):
    cursor = conn.cursor()
    
    # Generate random code if not provided
    if not group.code:
        # Get a random 4-digit code not already in use
        while True:
            code = random.randint(1000, 9999)
            cursor.execute("SELECT * FROM GroupTable WHERE code = ?", (code,))
            if not cursor.fetchone():
                break
    else:
        code = group.code
        # Check if code already exists
        cursor.execute("SELECT * FROM GroupTable WHERE code = ?", (code,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Group code already in use")
    
    # Insert group
    cursor.execute("INSERT INTO GroupTable (code) VALUES (?)", (code,))
    
    # Add creator to group
    cursor.execute(
        "INSERT INTO UGroup (email, code) VALUES (?, ?)",
        (current_user["email"], code)
    )
    
    conn.commit()
    
    return {"code": code, "members": [current_user["email"]]}

@app.post("/groups/join", response_model=Group)
async def join_group(
    group_code: int = Body(..., embed=True),
    current_user = Depends(get_current_user),
    conn = Depends(get_db)
):
    cursor = conn.cursor()
    
    # Check if group exists
    cursor.execute("SELECT * FROM GroupTable WHERE code = ?", (group_code,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if user is already in group
    cursor.execute(
        "SELECT * FROM UGroup WHERE email = ? AND code = ?",
        (current_user["email"], group_code)
    )
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already in group")
    
    # Check if group is full (limit to 10 members)
    cursor.execute("SELECT COUNT(*) FROM UGroup WHERE code = ?", (group_code,))
    count = cursor.fetchone()[0]
    if count >= 10:
        raise HTTPException(status_code=400, detail="Group is full")
    
    # Add user to group
    cursor.execute(
        "INSERT INTO UGroup (email, code) VALUES (?, ?)",
        (current_user["email"], group_code)
    )
    
    conn.commit()
    
    # Get all members
    cursor.execute("SELECT email FROM UGroup WHERE code = ?", (group_code,))
    members = [row["email"] for row in cursor.fetchall()]
    
    return {"code": group_code, "members": members}

@app.get("/groups", response_model=List[Group])
async def get_user_groups(
    current_user = Depends(get_current_user),
    conn = Depends(get_db)
):
    cursor = conn.cursor()
    
    # Get groups user is in
    cursor.execute(
        "SELECT code FROM UGroup WHERE email = ?",
        (current_user["email"],)
    )
    group_codes = [row["code"] for row in cursor.fetchall()]
    
    groups = []
    for code in group_codes:
        # Get members for each group
        cursor.execute("SELECT email FROM UGroup WHERE code = ?", (code,))
        members = [row["email"] for row in cursor.fetchall()]
        
        groups.append({
            "code": code,
            "members": members
        })
    
    return groups

@app.get("/groups/{group_code}/recommendations", response_model=List[City])
async def get_group_recommendations(
    group_code: int,
    current_user = Depends(get_current_user),
    conn = Depends(get_db),
    limit: int = Query(10, ge=1, le=30)
):
    cursor = conn.cursor()
    
    # Check if group exists
    cursor.execute("SELECT * FROM GroupTable WHERE code = ?", (group_code,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if user is in group
    cursor.execute(
        "SELECT * FROM UGroup WHERE email = ? AND code = ?",
        (current_user["email"], group_code)
    )
    if not cursor.fetchone():
        raise HTTPException(status_code=403, detail="User not in group")
    
    return get_group_recommended_cities(conn, group_code, limit)

@app.post("/flights/search", response_model=List[Flight])
async def search_flights(
    search: FlightSearch,
    current_user = Depends(get_current_user),
    conn = Depends(get_db)
):
    cursor = conn.cursor()
    
    # Build query parameters
    query = """
    SELECT * FROM Flight 
    WHERE depCity = ? 
    AND depTime BETWEEN ? AND ?
    """
    params = [search.departure_city, search.min_date, search.max_date]
    
    # Add budget constraint if provided
    if search.max_budget:
        query += " AND cost <= ?"
        params.append(search.max_budget)
    
    # Add companies filter if provided
    if search.companies and len(search.companies) > 0:
        query += " AND company IN ({})".format(','.join('?' for _ in search.companies))
        params.extend(search.companies)
    
    # Execute query
    cursor.execute(query, params)
    
    # Convert to list of Flight objects
    flights = []
    for row in cursor.fetchall():
        flights.append({
            "code": row["code"],
            "cost": row["cost"],
            "depCity": row["depCity"],
            "arrCity": row["arrCity"],
            "depTime": row["depTime"],
            "timeDuration": row["timeDuration"],
            "distance": row["distance"],
            "planeModel": row["planeModel"],
            "company": row["company"]
        })
    
    return flights

@app.get("/flight_companies", response_model=List[str])
async def get_flight_companies(conn = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM FlightCompany")
    return [row["name"] for row in cursor.fetchall()]

# Start the server with: uvicorn app:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 