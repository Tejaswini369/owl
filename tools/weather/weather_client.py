import logging
from typing import Dict, List, Optional, Union
from datetime import datetime
import requests
from ..common.base_client import BaseClient

logger = logging.getLogger(__name__)

class WeatherClient(BaseClient):
    """Client for fetching and processing weather data."""
    
    def __init__(self):
        """Initialize the weather client."""
        super().__init__()
        self.base_url = "https://api.open-meteo.com/v1"
        
    async def get_current_weather(self, location: str) -> Dict:
        """
        Get current weather for a location.
        
        Args:
            location: City name or coordinates (lat,lon)
            
        Returns:
            Dict containing current weather data
        """
        try:
            # First get coordinates from location name
            coords = await self._get_coordinates(location)
            if not coords:
                return None
                
            params = {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code", "wind_speed_10m"],
                "timezone": "auto"
            }
            
            response = await self._make_request(
                f"{self.base_url}/forecast",
                params=params
            )
            
            if response:
                return {
                    "location": location,
                    "temperature": response["current"]["temperature_2m"],
                    "feels_like": response["current"]["apparent_temperature"],
                    "humidity": response["current"]["relative_humidity_2m"],
                    "description": self._get_weather_description(response["current"]["weather_code"]),
                    "wind_speed": response["current"]["wind_speed_10m"],
                    "timestamp": datetime.now().isoformat()
                }
            return None
            
        except Exception as e:
            logger.error(f"Error fetching current weather: {str(e)}")
            return None
            
    async def get_forecast(self, location: str, days: int = 5) -> List[Dict]:
        """
        Get weather forecast for a location.
        
        Args:
            location: City name or coordinates (lat,lon)
            days: Number of days to forecast (max 5)
            
        Returns:
            List of forecast data for each day
        """
        try:
            coords = await self._get_coordinates(location)
            if not coords:
                return None
                
            params = {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code", "wind_speed_10m_max"],
                "timezone": "auto"
            }
            
            response = await self._make_request(
                f"{self.base_url}/forecast",
                params=params
            )
            
            if response:
                forecasts = []
                for i in range(min(days, len(response["daily"]["time"]))):
                    forecasts.append({
                        "timestamp": response["daily"]["time"][i],
                        "temperature_max": response["daily"]["temperature_2m_max"][i],
                        "temperature_min": response["daily"]["temperature_2m_min"][i],
                        "description": self._get_weather_description(response["daily"]["weather_code"][i]),
                        "wind_speed": response["daily"]["wind_speed_10m_max"][i]
                    })
                return forecasts
            return None
            
        except Exception as e:
            logger.error(f"Error fetching forecast: {str(e)}")
            return None
            
    async def get_air_quality(self, location: str) -> Dict:
        """
        Get air quality data for a location.
        
        Args:
            location: City name or coordinates (lat,lon)
            
        Returns:
            Dict containing air quality data
        """
        try:
            coords = await self._get_coordinates(location)
            if not coords:
                return None
                
            params = {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "current": ["pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone"],
                "timezone": "auto"
            }
            
            response = await self._make_request(
                f"{self.base_url}/air-quality",
                params=params
            )
            
            if response:
                components = response["current"]
                aqi = self._calculate_aqi(components)
                return {
                    "location": location,
                    "aqi": aqi,
                    "aqi_level": self._get_aqi_level(aqi),
                    "components": {
                        "pm10": components["pm10"],
                        "pm2_5": components["pm2_5"],
                        "co": components["carbon_monoxide"],
                        "no2": components["nitrogen_dioxide"],
                        "so2": components["sulphur_dioxide"],
                        "o3": components["ozone"]
                    },
                    "timestamp": datetime.now().isoformat()
                }
            return None
            
        except Exception as e:
            logger.error(f"Error fetching air quality: {str(e)}")
            return None
            
    async def _get_coordinates(self, location: str) -> Optional[Dict]:
        """Get coordinates for a location name."""
        try:
            # Use OpenStreetMap Nominatim API for geocoding
            params = {
                "q": location,
                "format": "json",
                "limit": 1
            }
            response = await self._make_request(
                "https://nominatim.openstreetmap.org/search",
                params=params
            )
            
            if response and len(response) > 0:
                return {
                    "latitude": float(response[0]["lat"]),
                    "longitude": float(response[0]["lon"])
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting coordinates: {str(e)}")
            return None
            
    def _get_weather_description(self, code: int) -> str:
        """Convert weather code to description."""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, "Unknown")
            
    def _calculate_aqi(self, components: Dict) -> int:
        """Calculate AQI from component values."""
        # Simple AQI calculation based on PM2.5 and PM10
        pm25 = components["pm2_5"]
        pm10 = components["pm10"]
        
        if pm25 <= 12 and pm10 <= 54:
            return 1  # Good
        elif pm25 <= 35.4 and pm10 <= 154:
            return 2  # Fair
        elif pm25 <= 55.4 and pm10 <= 254:
            return 3  # Moderate
        elif pm25 <= 150.4 and pm10 <= 354:
            return 4  # Poor
        else:
            return 5  # Very Poor
            
    def _get_aqi_level(self, aqi: int) -> str:
        """Convert AQI number to level description."""
        levels = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        return levels.get(aqi, "Unknown") 