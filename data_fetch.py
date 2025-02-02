import requests
import json

# API Endpoints
API_ENDPOINTS = {
    "quiz_data": "https://api.jsonserve.com/XgAgFJ",
    "quiz_submission": "https://api.jsonserve.com/rJvd7g",
    "quiz_all_data": "https://www.jsonkeeper.com/b/LLQT"
}

# Function to fetch data from an API
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error if request fails
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Fetch and store data
quiz_data = fetch_data(API_ENDPOINTS["quiz_data"])
quiz_submission = fetch_data(API_ENDPOINTS["quiz_submission"])
quiz_all_data = fetch_data(API_ENDPOINTS["quiz_all_data"])

# Save to JSON files for local analysis
if quiz_data:
    with open("quiz_data.json", "w") as f:
        json.dump(quiz_data, f, indent=4)

if quiz_submission:
    with open("quiz_submission.json", "w") as f:
        json.dump(quiz_submission, f, indent=4)

if quiz_all_data:
    with open("quiz_all_data.json", "w") as f:
        json.dump(quiz_all_data, f, indent=4)

print("Data fetched and saved successfully!")
