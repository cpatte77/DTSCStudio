import os
from dotenv import load_dotenv

load_dotenv()
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY")[:6] + "...")  # safe debug
print("OPENAI_BASE_URL:", os.getenv("OPENAI_BASE_URL"))
print("OPENAI_DEPLOYMENT:", os.getenv("OPENAI_DEPLOYMENT"))
