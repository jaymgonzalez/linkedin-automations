import requests
import dotenv
import os
import json
import pandas as pd

dotenv.load_dotenv()
token = os.environ.get("CRAWLBASE_TOKEN")

df = pd.read_csv("phantombuster-all-leads-02112024.csv")

linkedin_urls = df["linkedinProfileUrl"]

linkedin_urls = (
    linkedin_urls.dropna()
    .apply(lambda x: x if x.startswith("https://linkedin.com") else None)
    .dropna()
    .tolist()
)

ids = []

# linkedin_urls = linkedin_urls[:1]


# print(ids)
def get_profile_rid(url):
    params = (
        ("token", token),
        # ("async", "true"),
        ("scraper", "linkedin-profile"),
        ("callback", "true"),
        ("crawler", "LinkedInProfileCrawler"),
        ("url", url),
        ("format", "json"),
    )

    try:
        response = requests.get("https://api.crawlbase.com", params=params)
        print(response.url)
        id = response.json()["rid"]

        print(id)

        return id

    except json.decoder.JSONDecodeError:
        print("There was an issue with the JSON object")
        print(url, response.text)

        return None


def get_profile_html(id):

    params = (
        ("token", token),
        ("rid", id),
        ("format", "json"),
    )

    response = requests.get("https://api.crawlbase.com/storage", params=params)
    print(response.text)


for url in linkedin_urls:
    ids.append(get_profile_rid(url))

print(ids)

for id in ids:
    get_profile_html(id)


get_profile_rid("https://linkedin.com/in/gerrieswart123")
get_profile_html("")


# create funtion to extrac json
