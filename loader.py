
# loader.py

import os
import json
from datetime import datetime, timezone
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd

# --- Load environment variables ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
JSON_FILE = "data/structured_data_clean.json"

# Load JSON data from file
try:
    # Open the JSON file in read mode ('r')
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)

    # Now 'data' contains the parsed content of your JSON file
    print("JSON data loaded successfully:")


except FileNotFoundError:
    print(f"Error: The file '{JSON_FILE}' was not found.")
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{JSON_FILE}'. Check for malformed JSON.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# print(pd.DataFrame.from_dict(data))
print(data)
print(type(data))


# Confirm it’s now a list
if not isinstance(data, dict):
    raise TypeError(f"Expected a list of records in JSON file, but got {type(data)}")

print(data['data'])
df = data['data']
df = pd.DataFrame(df)
df.to_csv('test_csv.csv')



# # Upsert into Supabase
# TABLE_NAME = "countries"
# response = supabase.table(TABLE_NAME).upsert(data, on_conflict="Country").execute()

import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime

# Load environment variables
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(url, key)

# Add/update timestamp column
df["updated_at"] = datetime.utcnow().isoformat()

# Convert to records for Supabase
records = df.to_dict(orient="records")

# Upsert into Supabase
try:
    response = supabase.table("countries").upsert(records).execute()
    print("✅ Upsert successful:", response)
except Exception as e:
    print("❌ Error upserting into Supabase:", e)

# if response.data:
#     print(f"✅ Success! Upserted {len(response.data)} records.")
# else:
#     print("⚠️ Upsert operation completed, but no data was returned by Supabase.")
