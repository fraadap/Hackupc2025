
import requests
import json
import random
import time

print("ciao")
# API Base URL
BASE_URL = "http://localhost:8000"

# Test data with timestamp to ensure uniqueness
TEST_USER = {
    "email": f"vote_tester_{int(time.time())}@example.com",
    "username": f"vote_tester_{int(time.time())}",
    "password": "password123"
}

# Helper functions
def print_response(description, response):
    print("\n" + "="*80)
    print(f"TEST: {description}")
    print(f"URL: {response.url}")
    print(f"Method: {response.request.method}")
    print(f"Status Code: {response.status_code}")
    try:
        json_response = response.json()
        print("Response Body:")
        print(json.dumps(json_response, indent=2))
    except:
        print("Response Body (not JSON):")
        print(response.text[:500])  # Print first 500 chars to avoid huge responses
    print("="*80 + "\n")
    return response

def make_request(method, endpoint, data=None, token=None, params=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    if method == "GET":
        response = requests.get(url, headers=headers, params=params)
    elif method == "POST":
        headers["Content-Type"] = "application/json"
        response = requests.post(url, json=data, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    return response

def register_user(user_data):
    response = make_request("POST", "/users", data=user_data)
    return print_response("Register User", response)

def login(email, password):
    data = {
        "username": email,  # Backend expects username field for email
        "password": password
    }
    response = requests.post(f"{BASE_URL}/token", data=data)
    return print_response("Login User", response)

def get_cities_for_evaluation(token, limit=5):
    params = {"limit": limit}
    response = make_request("GET", "/cities/evaluation", token=token, params=params)
    return print_response("Get Cities for Evaluation", response)

def vote_city(token, city, value):
    data = {"city": city, "value": value}
    response = make_request("POST", "/cities/vote", token=token, data=data)
    return print_response(f"Vote City: {city} (value: {value})", response)

def get_recommendations(token, limit=10):
    params = {"limit": limit}
    response = make_request("GET", "/recommendations", token=token, params=params)
    return print_response("Get Recommendations", response)

def get_all_cities(token):
    response = make_request("GET", "/cities", token=token)
    return print_response("Get All Cities", response)

def check_database():
    """Test if the database has cities by calling the /cities endpoint without authentication"""
    response = requests.get(f"{BASE_URL}/cities")
    print("\n" + "="*80)
    print("TEST: Check Database for Cities")
    print(f"Status Code: {response.status_code}")
    
    try:
        cities = response.json()
        print(f"Number of cities in database: {len(cities)}")
        if len(cities) > 0:
            print(f"Sample cities: {', '.join(cities[:5])}")
        else:
            print("WARNING: No cities found in database. You need to run generate_data.py first.")
    except:
        print("ERROR: Could not parse response as JSON. Database may not be initialized.")
        print(response.text[:200])
    
    print("="*80 + "\n")
    return response

def test_city_voting_workflow():
    print("\n" + "#"*100)
    print("TESTING CITY EVALUATION AND VOTING WORKFLOW")
    print("#"*100 + "\n")
    
    # First, check if we have cities in the database
    print(">>> Checking Database <<<")
    db_check = check_database()
    if db_check.status_code != 200 or len(db_check.json()) == 0:
        print("❌ Database appears to be empty or not accessible. Run generate_data.py first.")
        print("Continuing tests anyway to see all errors...")
    
    # 1. Register a test user
    print("\n>>> Step 1: Registering Test User <<<")
    register_response = register_user(TEST_USER)
    
    # 2. Login to get token
    print("\n>>> Step 2: Logging In <<<")
    login_response = login(TEST_USER["email"], TEST_USER["password"])
    
    if login_response.status_code != 200:
        print("❌ LOGIN FAILED! Cannot continue with authenticated requests.")
        return
    
    token = login_response.json()["access_token"]
    
    # 3. Get all cities (check if database is populated)
    print("\n>>> Step 3: Get All Cities <<<")
    cities_response = get_all_cities(token)
    cities = cities_response.json() if cities_response.status_code == 200 else []
    
    if not cities:
        print("❌ No cities found in database. Make sure to run generate_data.py first.")
    
    # 4. Get cities for evaluation
    print("\n>>> Step 4: Get Cities for Evaluation <<<")
    eval_response = get_cities_for_evaluation(token)
    eval_cities = eval_response.json() if eval_response.status_code == 200 else []
    
    if not eval_cities:
        print("❌ No cities returned for evaluation. This could be an API error.")
        
        # Try to inspect the response for clues
        print("\nDEBUG INFO:")
        print(f"Response status: {eval_response.status_code}")
        print(f"Response text: {eval_response.text[:500]}")
        
        # Get the raw SQL query from app.py to help debug
        print("\nIn app.py, the SQL query for cities/evaluation is:")
        print("cursor.execute(\"SELECT name FROM City WHERE name NOT IN ({})\".format(")
        print("    ','.join('?' for _ in voted_cities) if voted_cities else \"''\"),")
        print("voted_cities if voted_cities else [])")
        
        # Try a manual vote anyway
        if cities:
            print("\n>>> Attempting a manual vote on the first city... <<<")
            test_city = cities[0]
            vote_city(token, test_city, 1)
    else:
        # 5. Vote on cities for evaluation
        print(f"\n>>> Step 5: Voting on {len(eval_cities)} Cities <<<")
        for i, city in enumerate(eval_cities):
            # Alternate between like (1) and dislike (0)
            vote_value = i % 2
            vote_city(token, city["name"], vote_value)
    
    # 6. Get recommendations based on votes
    print("\n>>> Step 6: Get Recommendations Based on Votes <<<")
    get_recommendations(token)
    
    # 7. Try to get more cities for evaluation (should be different ones)
    print("\n>>> Step 7: Get More Cities for Evaluation <<<")
    more_eval_response = get_cities_for_evaluation(token)
    more_eval_cities = more_eval_response.json() if more_eval_response.status_code == 200 else []
    
    print(f"Got {len(more_eval_cities)} new cities for evaluation")
    
    # Check if we got new cities or the same ones
    if eval_cities and more_eval_cities:
        first_batch = set(city["name"] for city in eval_cities)
        second_batch = set(city["name"] for city in more_eval_cities)
        overlap = first_batch.intersection(second_batch)
        
        if overlap:
            print(f"❌ ERROR: Found {len(overlap)} cities that were already evaluated but returned again:")
            print(", ".join(overlap))
            print("This suggests the voting was not properly recorded.")
        else:
            print("✅ SUCCESS: Got completely new set of cities for evaluation!")
    
    print("\n" + "#"*100)
    print("CITY EVALUATION AND VOTING TEST COMPLETED")
    print("#"*100 + "\n")

if __name__ == "__main__":
    try:
        test_city_voting_workflow()
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH ERROR: {str(e)}")
        import traceback
        traceback.print_exc() 