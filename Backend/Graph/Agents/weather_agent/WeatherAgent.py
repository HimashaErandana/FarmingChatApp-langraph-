from ..BaseAgent import BaseAgent
import httpx
from services.llm_service import invoke_llm
from pydantic import BaseModel
from config import OPENWEATHER_API_KEY
class Weather(BaseModel):
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    condition: str
    wind_speed: float
    rain: float
    alert: str


class WeatherAgent(BaseAgent):


    def call(self,q) -> Weather:

        city = invoke_llm(f"""
            Extract the name of the city from the following question. 
            - Return **only the city name**. 
            - Do not include any extra words, punctuation, or explanation. 
            - If no city is mentioned, return "unknown".

            Question: "{q}"
            """)
        
        '''call llm here to extract the city and day using query'''

        api_key = OPENWEATHER_API_KEY

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        res = httpx.get(url)
        api_response = res.json()
        print(api_response)
        weather = Weather(
        city=api_response.get("name"),
        country=api_response.get("sys", {}).get("country"),
        temperature=api_response.get("main", {}).get("temp"),
        feels_like=api_response.get("main", {}).get("feels_like"),
        humidity=api_response.get("main", {}).get("humidity"),
        condition=api_response.get("weather")[0].get("description"),
        wind_speed=api_response.get("wind", {}).get("speed"),
        rain=api_response.get("rain", {}).get("1h", 0),  # default 0 if no rain
        alert=""  # you can fill this later if you have alert info
        )

        #llm_res = invoke_llm(f"use this weather obj {weather.model_dump_json()} and asnwer this question {q}")
       
        return weather.model_dump_json()