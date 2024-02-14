import requests
import dotenv
import os
import json
import re
import pandas as pd
from openai import OpenAI
import instructor
from pydantic import BaseModel, Field
from typing import List


# models.py
class Activity(BaseModel):
    """Represents a LinkedIn activity."""

    title: str


class Experience(BaseModel):
    """Represents a LinkedIn experience."""

    title: str
    company: str
    date_range: str
    location: str
    description: str


class LinkedInProfile(BaseModel):
    name: str
    headline: str
    summary: str
    location: str
    industry: str
    education: List[str]
    experience: List[Experience] = Field(max_items=3)
    activities: List[Activity]
    followers: int


dotenv.load_dotenv()
token = os.environ.get("CRAWLBASE_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = instructor.patch(OpenAI(api_key=OPENAI_API_KEY))


def get_urls(df, column_name):
    linkedin_urls = df[column_name]

    linkedin_urls = (
        linkedin_urls.dropna()
        .apply(lambda x: x if x.startswith("https://www.linkedin.com") else None)
        .dropna()
        .tolist()
    )

    return linkedin_urls


def get_ids(df, column_name):
    ids = df[column_name]

    ids = ids.dropna().tolist()

    return ids


def create_columns(df, columns):
    for column in columns:
        if column not in df.columns:
            df[column] = None

    return df


def set_profile_rid(url):
    params = (
        ("token", token),
        ("scraper", "linkedin-profile"),
        ("callback", "true"),
        ("crawler", "LinkedInProfileCrawler"),
        ("url", url),
        ("format", "json"),
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


def get_profile_json(id):
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
        print(f"There was an issue with the request: {e}")
        print(id, response.text)

        return None


def check_if_exists(index, df, column_name):
    return pd.notna(df.at[index[0], column_name])


def remove_links_and_specific_key(d, target_key="peopleAlsoViewed"):
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    for key in list(
        d.keys()
    ):  # Use list(d.keys()) to avoid RuntimeError during iteration
        if key == target_key:
            del d[key]  # Remove the specific key
            continue  # Skip further checks and continue with the next iteration
        if isinstance(d[key], dict):
            d[key] = remove_links_and_specific_key(d[key], target_key)
        elif isinstance(d[key], list):
            d[key] = [
                (
                    remove_links_and_specific_key(item, target_key)
                    if isinstance(item, dict)
                    else item
                )
                for item in d[key]
            ]
        elif isinstance(d[key], str) and url_pattern.search(d[key]):
            del d[key]  # Remove key if value is a URL
    return d


def append_item_to_row(df, item, id, column_id, column_name):
    index = df[df[column_id] == id].index
    if not index.empty:
        df.at[index[0], column_name] = item

    return df


def synthesize_profile(profile):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_model=LinkedInProfile,
            messages=[
                {
                    "role": "system",
                    "content": "Given a JSON representation of a LinkedIn profile, extract and synthesize the most relevant information to be used in crafting a personalized connection request message\nhighlighting the information that could make a connection request more personalized and engaging\nmake sure to add the recent posts if any in activities\ndo not include http links",
                },
                {
                    "role": "user",
                    "content": f"###profile### \n\n {profile} \n\n ###profile###",
                },
            ],
        )
        print(response)
        return response.model_dump_json(indent=2)

    except Exception as e:
        print(e)
        return None


def update_csv_with_rid(csv_name, column_name="linkedinUrl"):
    df = pd.read_csv(csv_name)

    create_columns(df, ["rid"])

    linkedin_urls = get_urls(df, column_name)

    linkedin_urls = linkedin_urls[:2]

    for url in linkedin_urls:

        if check_if_exists(df[df[column_name] == url].index, df, "rid"):
            continue
        else:

            id = set_profile_rid(url)
            # the id in this case is the URL
            append_item_to_row(df, id, url, column_name, "rid")

    df.to_csv(csv_name, index=False)


def update_csv_with_profile(csv_name, column_name="rid"):
    df = pd.read_csv(csv_name)

    ids = get_ids(df, column_name)

    for id in ids:
        profile = get_profile_json(id)

        if profile is None:
            continue

        profile = json.loads(profile)
        # print(type(profile))

        df = append_item_to_row(df, profile, id, column_name, "linkedinProfile")

        profile = remove_links_and_specific_key(profile)

        profile = json.dumps(profile)

        df = append_item_to_row(
            df, synthesize_profile(profile), id, column_name, "synthesizedProfile"
        )

    df.to_csv(csv_name, index=False)


if __name__ == "__main__":
    # update_csv_with_rid("freelanceSpain.csv")
    update_csv_with_profile("freelanceSpain.csv")
