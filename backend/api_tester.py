
import requests
import json
import random
import time
from datetime import datetime, timedelta

# API Base URL
BASE_URL = "http://localhost:8000"

# Test data
TEST_USER = {
    "email": f"test_user_{int(time.time())}@example.com",
    "username": f"test_user_{int(time.time())}",
    "password": "password123"
}

TEST_USER2 = {
    "email": f"test_user2_{int(time.time())}@example.com",
    "username": f"test_user2_{int(time.time())}",
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

# Test functions
def test_register_user(user_data):
    response = make_request("POST", "/users", data=user_data)
    return print_response("Register User", response)

def test_login(email, password):
    data = {
        "username": email,  # Backend expects username field for email
        "password": password
    }
    response = requests.post(f"{BASE_URL}/token", data=data)
    return print_response("Login User", response)

def test_current_user(token):
    response = make_request("GET", "/users/me", token=token)
    return print_response("Get Current User", response)

def test_get_cities(token):
    response = make_request("GET", "/cities", token=token)
    return print_response("Get All Cities", response)

def test_get_city_by_name(token, city_name):
    response = make_request("GET", f"/cities/{city_name}", token=token)
    return print_response(f"Get City: {city_name}", response)

def test_get_cities_for_evaluation(token, limit=5):
    params = {"limit": limit}
    response = make_request("GET", "/cities/evaluation", token=token, params=params)
    return print_response("Get Cities for Evaluation", response)

def test_vote_city(token, city, value):
    data = {"city": city, "value": value}
    response = make_request("POST", "/cities/vote", token=token, data=data)
    return print_response(f"Vote City: {city} (value: {value})", response)

def test_get_recommendations(token, limit=10):
    params = {"limit": limit}
    response = make_request("GET", "/recommendations", token=token, params=params)
    return print_response("Get Recommendations", response)

def test_create_group(token, code=None):
    data = {"code": code} if code else {}
    response = make_request("POST", "/groups", token=token, data=data)
    return print_response("Create Group", response)

def test_join_group(token, group_code):
    data = {"group_code": group_code}
    response = make_request("POST", "/groups/join", token=token, data=data)
    return print_response(f"Join Group: {group_code}", response)

def test_get_user_groups(token):
    response = make_request("GET", "/groups", token=token)
    return print_response("Get User Groups", response)

def test_get_group_recommendations(token, group_code, limit=10):
    params = {"limit": limit}
    response = make_request("GET", f"/groups/{group_code}/recommendations", token=token, params=params)
    return print_response(f"Get Group Recommendations: {group_code}", response)

def test_get_flight_companies(token):
    response = make_request("GET", "/flight_companies", token=token)
    return print_response("Get Flight Companies", response)

def test_search_flights(token, departure_city, min_date, max_date, max_budget=None, companies=None):
    data = {
        "departure_city": departure_city,
        "min_date": min_date,
        "max_date": max_date
    }
    if max_budget:
        data["max_budget"] = max_budget
    if companies:
        data["companies"] = companies
        
    response = make_request("POST", "/flights/search", token=token, data=data)
    return print_response(f"Search Flights from {departure_city}", response)

def run_full_user_journey_test():
    print("\n" + "#"*100)
    print("STARTING FULL API TEST SUITE")
    print("#"*100 + "\n")
    
    # 1. Register two test users
    print("\n>>> Testing User Registration <<<")
    test_register_user(TEST_USER)
    test_register_user(TEST_USER2)
    
    # 2. Login and get tokens
    print("\n>>> Testing User Authentication <<<")
    login_response = test_login(TEST_USER["email"], TEST_USER["password"])
    if login_response.status_code != 200:
        print("❌ LOGIN FAILED! Aborting tests...")
        return
    
    token = login_response.json()["access_token"]
    login_response2 = test_login(TEST_USER2["email"], TEST_USER2["password"])
    if login_response2.status_code != 200:
        print("❌ SECOND USER LOGIN FAILED! Continuing with one user...")
        token2 = None
    else:
        token2 = login_response2.json()["access_token"]
    
    # 3. Get current user info
    print("\n>>> Testing User Profile <<<")
    test_current_user(token)
    
    # 4. Get all cities
    print("\n>>> Testing Cities Endpoints <<<")
    cities_response = test_get_cities(token)
    cities = cities_response.json() if cities_response.status_code == 200 else []
    
    # 5. Get a specific city (if available)
    if cities and len(cities) > 0:
        test_get_city_by_name(token, cities[0])
    else:
        print("No cities available to test city details endpoint")
    
    # 6. Get cities for evaluation
    evaluation_response = test_get_cities_for_evaluation(token)
    evaluation_cities = evaluation_response.json() if evaluation_response.status_code == 200 else []
    
    # 7. Vote on cities
    print("\n>>> Testing City Voting <<<")
    if evaluation_cities and len(evaluation_cities) > 0:
        for i, city in enumerate(evaluation_cities):
            # Alternate between like (1) and dislike (0)
            vote_value = i % 2  
            test_vote_city(token, city["name"], vote_value)
    else:
        print("No evaluation cities available to test voting")
    
    # 8. Get recommendations
    print("\n>>> Testing Recommendations <<<")
    test_get_recommendations(token)
    
    # 9. Create a group
    print("\n>>> Testing Group Features <<<")
    group_response = test_create_group(token)
    if group_response.status_code == 200:
        group_code = group_response.json()["code"]
        
        # 10. Second user joins the group (if we have a second user)
        if token2:
            test_join_group(token2, group_code)
        
        # 11. Get user groups
        test_get_user_groups(token)
        
        # 12. Get group recommendations
        test_get_group_recommendations(token, group_code)
    else:
        print("Group creation failed, skipping group tests")
    
    # 13. Get flight companies
    print("\n>>> Testing Flight Features <<<")
    companies_response = test_get_flight_companies(token)
    companies = companies_response.json() if companies_response.status_code == 200 else []
    
    # 14. Search flights
    if cities and len(cities) > 0:
        # Generate dates for next month
        today = datetime.now()
        min_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")
        max_date = (today + timedelta(days=60)).strftime("%Y-%m-%d")
        
        test_search_flights(
            token, 
            departure_city=cities[0], 
            min_date=min_date, 
            max_date=max_date,
            max_budget=1000, 
            companies=companies[:2] if len(companies) >= 2 else None
        )
    else:
        print("No cities available to test flight search")
    
    print("\n" + "#"*100)
    print("API TEST SUITE COMPLETED")
    print("#"*100 + "\n")

if __name__ == "__main__":
    try:
        run_full_user_journey_test()
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH ERROR: {str(e)}") 