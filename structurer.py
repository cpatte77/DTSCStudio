# structurer.py

import json
from pathlib import Path
from openai import OpenAI

RAW_BLOB = Path("data/raw_blob.txt")
OUT_JSON = Path("data/structured_data.json")

def main():
    # --- Client Setup ---
    endpoint = "https://cdong1--azure-proxy-web-app.modal.run"
    api_key = "supersecretkey"
    deployment_name = "gpt-4o"
    client = OpenAI(base_url=endpoint, api_key=api_key)

    # --- Read Raw Data ---
    with open(RAW_BLOB, "r", encoding="utf-8") as f:
        blob = f.read()

    # --- Create Prompt ---
    system_prompt = "Return a clean JSON array of objects with keys 'name', 'capital', 'population', and 'area'. Do not add any extra text or markdown."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": blob}
    ]

    # --- Get Structured Data from LLM ---
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        response_format={"type": "json_object"}
    )
    llm_output_str = response.choices[0].message.content

    try:
        # 1. (CRITICAL) Convert the AI's text string into a Python list
        structured_data = json.loads(llm_output_str)

        # Handle if the AI wraps the list in a dictionary like {"countries": [...]}
        if isinstance(structured_data, dict) and len(structured_data) == 1:
            key = list(structured_data.keys())[0]
            if isinstance(structured_data[key], list):
                 structured_data = structured_data[key]

        # 2. (CRITICAL) Save the Python list to the file as a proper JSON array
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        with open(OUT_JSON, "w", encoding="utf-8") as f:
            json.dump(structured_data, f, indent=2)

        print(f"✅ Success! Wrote {len(structured_data)} records to {OUT_JSON.resolve()}")

    except json.JSONDecodeError:
        print(f"❌ Error: Failed to parse the AI's response as JSON.")
        print("--- AI Raw Output ---")
        print(llm_output_str)

if __name__ == "__main__":
    main()