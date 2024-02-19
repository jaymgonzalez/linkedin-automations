import os
import instructor
import dotenv
from openai import OpenAI
from app.models import LinkedInProfile, ConnectionRequestMessage

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = instructor.patch(OpenAI(api_key=OPENAI_API_KEY))


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


def create_connection_request_message(profile):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_model=ConnectionRequestMessage,
            messages=[
                {
                    "role": "system",
                    "content": "you are an expert in crafting personalized connection request messages\nplease create a personalized connection request message using the given profile\nuse data from the sender to personalize the message if appropiate\nkeep the message short and engaging\ninclude relevant topics only\nCreate short sentences\nMax 15 words per sentence",
                },
                {
                    "role": "user",
                    "content": "###sender### \n\n technical freelancer building linkedin brands for other freelancers talking about business and personal development. have worked as a devops engineer and solutions engineer \n\n ###sender###",
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
