import asyncio
import logging
from weather_client import WeatherClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Initialize the weather client
    client = WeatherClient()
    
    # Test location
    location = "London,UK"
    
    try:
        # Get current weather
        logger.info(f"\nFetching current weather for {location}...")
        current_weather = await client.get_current_weather(location)
        
        if current_weather:
            print("\nCurrent Weather:")
            print(f"Location: {current_weather['location']}")
            print(f"Temperature: {current_weather['temperature']}°C")
            print(f"Feels like: {current_weather['feels_like']}°C")
            print(f"Humidity: {current_weather['humidity']}%")
            print(f"Description: {current_weather['description']}")
            print(f"Wind Speed: {current_weather['wind_speed']} m/s")
            print(f"Last Updated: {current_weather['timestamp']}")
        
        # Get forecast
        logger.info(f"\nFetching 5-day forecast for {location}...")
        forecast = await client.get_forecast(location, days=5)
        
        if forecast:
            print("\nForecast:")
            for day in forecast:
                print(f"\nDate: {day['timestamp']}")
                print(f"Temperature: {day['temperature_min']}°C to {day['temperature_max']}°C")
                print(f"Description: {day['description']}")
                print(f"Wind Speed: {day['wind_speed']} m/s")
        
        # Get air quality
        logger.info(f"\nFetching air quality data for {location}...")
        air_quality = await client.get_air_quality(location)
        
        if air_quality:
            print("\nAir Quality:")
            print(f"Location: {air_quality['location']}")
            print(f"AQI: {air_quality['aqi']} ({air_quality['aqi_level']})")
            print("Components:")
            for component, value in air_quality['components'].items():
                print(f"  {component}: {value}")
            print(f"Last Updated: {air_quality['timestamp']}")
            
    except Exception as e:
        logger.error(f"Error in weather test: {str(e)}")
    finally:
        # Cleanup
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 