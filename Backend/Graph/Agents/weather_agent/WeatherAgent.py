from ..BaseAgent import BaseAgent
import httpx

from pydantic import BaseModel

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

    url = "https://api.openweathermap.org/data/2.5/weather?q=kandy&appid=3dca038969f319eb781a0c0fa3bc9899&units=metric"

    async def call(self,state) -> Weather:

        q = state['user_query']

        '''call llm here to extract the city and day using query'''

        async with httpx.AsyncClient as client:
            api_response = await client.get(self.url)

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

        return weather