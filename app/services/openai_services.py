import json
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
            temperature=0.2,
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


def create_connection_request_message(profile, first_name):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            response_model=ConnectionRequestMessage,
            messages=[
                {
                    "role": "system",
                    "content": "you are an expert in crafting personalized connection request messages\nplease create a connection request message using the given profile\nkeep the message short and engaging\ninclude relevant topics only\nCreate short sentences\nMax 15 words per sentence\nuse sender information only if it is relevant\n",
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

        message = response.model_dump_json(indent=2)
        message = json.loads(message)

        final_message = f"Hi {first_name.split()[0]} 👋\n{message['first_sentence']}\n{message['second_sentence']}\n{message['closer']}"

        return final_message

    except Exception as e:
        print(e)
        return None
