from dotenv import load_dotenv
import os
import requests
from google import genai
from google.genai import types

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str) -> str:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "es"
    }

    if not OPENWEATHER_API_KEY:
        raise ValueError("OPENWEATHER_API_KEY no está definida en el .env")
    
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return f"No pude obtener el clima de {city}. Error: {response.text}"

    data = response.json()

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]

    return (
        f"Clima actual en {city}: {description}. "
        f"Temperatura: {temp}°C, sensación térmica: {feels_like}°C, "
        f"humedad: {humidity}%."
    )

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

weather_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="Obtiene el clima actual en tiempo real de una ciudad",
            parameters={
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        )
    ]
)

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="Eres un asistente que responde usando herramientas cuando sea necesario.",
        tools=[weather_tool]
    )
)

response = chat.send_message("What is the weather in Roma?")

# Validar si pidió tool call
part = response.candidates[0].content.parts[0]

if part.function_call:
    fc = part.function_call
    print("Gemini pidió llamar función:", fc.name, fc.args)

    if fc.name == "get_weather":
        tool_result = get_weather(fc.args["city"])

        response2 = chat.send_message(
            types.Part.from_function_response(
                name="get_weather",
                response={"result": tool_result}
            )
        )

        print(response2.text)

else:
    print(response.text)