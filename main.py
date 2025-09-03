from supabase import create_client, Client
import pandas as pd

# -------------------------------
# Replace these with your Supabase info
SUPABASE_URL = "https://gkeypywncyvlxnuwrddt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdrZXlweXduY3l2bHhudXdyZGR0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3MTUxNjcsImV4cCI6MjA3MTI5MTE2N30.ac98XW-c-NMNfaMO1zbQFlaNxqjK2SSm9_dHqQfNN9w"
TABLE_NAME = "drama_films"
# -------------------------------

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch all rows from the table
data = supabase.table(TABLE_NAME).select("*").execute()

# Convert to pandas DataFrame
df = pd.DataFrame(data.data)

# Show first 5 rows
print(df.head())
