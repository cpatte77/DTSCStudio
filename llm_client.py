from openai import OpenAI

endpoint = "https://cdong1--azure-proxy-web-app.modal.run"
api_key = "supersecretkey"
deployment_name = "gpt-4o"

client = OpenAI(base_url=endpoint, api_key=api_key)

def get_openai_client():
    return client, deployment_name

from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("OPENAI_API_KEY"))