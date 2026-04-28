from dotenv import load_dotenv
import os
import requests
import json
import time

load_dotenv()

API_KEY = os.getenv("SPIDRAIO_KEY")

payload = {
    "urls": [{"url": "https://books.toscrape.com/"}],
    "prompt": "Extract all books on this page. For each book, return the title, price, and star rating as a number from 1 to 5.",
    "output": "json"
}

response = requests.post(
    "https://api.spidra.io/api/scrape",
    headers={
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    },
    json=payload
)

if not API_KEY:
    raise ValueError("API KEY no cargada desde .env")

print(response.status_code)
print(response.text)

data = response.json()
print(json.dumps(data, indent=2))


##### Se confirma la peticion asincrona a la API enviando el "jod_id".
job_id = data["jobId"]

url = f"https://api.spidra.io/api/scrape/{job_id}"

while True:
    response = requests.get(
        url,
        headers={
            "x-api-key": API_KEY,  # ⚠️ mismo header que funcionó antes
        }
    )

    result = response.json()

    print("Estado:", result.get("status"))

    if result.get("status") == "completed":
        print("✅ RESULTADO FINAL:")
        print(json.dumps(result, indent=2))
        break

    elif result.get("status") == "error":
        print("❌ Error:", result)
        break

    time.sleep(8)  # espera 2 segundos antes de volver a consultar
