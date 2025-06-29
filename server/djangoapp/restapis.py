import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030"
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"

    request_url = backend_url + endpoint + "?" + params

    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url)
        if 'sentiment' in response.json():
            return response.json()
        else:
            return {"sentiment": "Error: Sentiment analysis failed"}
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to sentiment analyzer: {e}")
        return {"sentiment": "Error: Failed to connect to sentiment analyzer"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"sentiment": "Error: An unexpected error occurred"}


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
