import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("CRAWLBASE_TOKEN")


def set_profile_rid(url):
    params = (
        ("token", token),
        ("scraper", "linkedin-profile"),
        ("callback", "true"),
        ("url", url),
        ("format", "json"),
        ("crawler", "LinkedInProfileCrawler"),
        # ("autoparse", "true"),
    )

    try:
        response = requests.get("https://api.crawlbase.com", params=params)
        id = response.json()["rid"]
        print(id)

        return id

    except json.decoder.JSONDecodeError:
        print("There was an issue with the JSON object")
        print(url, response.text)

        return None

    except Exception as e:
        print(f"There was an issue with the request: {e}")
        print(url, response.text)

        return None


def get_json_from_id(id):
    params = (
        ("token", token),
        ("rid", id),
        ("format", "json"),
    )

    try:
        response = requests.get("https://api.crawlbase.com/storage", params=params)
        profile = response.json()["body"]

        profile = json.loads(profile)["body"]
        print(profile)

        return profile

    except json.decoder.JSONDecodeError:
        print("There was an issue with the JSON object")
        print(id, response.text)

        return None

    except Exception as e:
        if response.json()["error"] == "Not Found":
            print(f"The profile with id {id} was not found")
            return None
        else:
            print(f"There was an issue with the request: {e}")
            print(id, response.text)

            return None


def set_feed_rid(id):
    params = (
        ("token", token),
        ("format", "json"),
        ("scraper", "linkedin-feed"),
        ("callback", "true"),
        ("url", f"https://www.linkedin.com/feed/update/urn:li:activity:{id}"),
        ("format", "json"),
        ("crawler", "LinkedInProfileCrawler"),
    )

    try:
        response = requests.get("https://api.crawlbase.com", params=params)

        id = response.json()["rid"]
        return id

    except json.decoder.JSONDecodeError:
        print("There was an issue with the JSON object")
        print(id, response.text)

        return None

    except Exception as e:
        if response.json()["error"] == "Not Found":
            print(f"The feed with id {id} was not found")
            return None
        else:
            print(f"There was an issue with the request: {e}")
            print(id, response.text)

        return None


# set_feed_rid("7165716189489418242")


# feed = get_json_from_id("55495856922760e2ec3cf38b843c3f")
