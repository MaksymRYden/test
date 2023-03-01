import aiogram
import requests

BOT_TOKEN = ""
OPENWEATHERMAP_API_KEY = ""

bot = aiogram.Bot(token=BOT_TOKEN)
dp = aiogram.Dispatcher(bot)

# "Help" buttons
custom_keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
help_button = aiogram.types.KeyboardButton("/help")
custom_keyboard.add(help_button)

@dp.message_handler(commands=["start"])
async def send_weather(message: aiogram.types.Message):
    try:
        location = message.text.split(" ")[1]
    except IndexError:
        await bot.send_message(message.chat.id, "Please enter a location after the command /start.", reply_markup=custom_keyboard)
        return

    # Query the OpenWeatherMap API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        await bot.send_message(message.chat.id, "Sorry, I couldn't get the weather for that location. Please try again.", reply_markup=custom_keyboard)
        return

    weather_data = response.json()
    weather_description = weather_data["weather"][0]["description"].capitalize()
    temperature = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    
    
    message_text = f"The weather in {location.title()} is {weather_description}.\n"
    message_text += f"Temperature: {temperature}°C\n"
    message_text += f"Feels like: {feels_like}°C\n"
    message_text += f"Humidity: {humidity}%\n"
    message_text += f"Wind speed: {wind_speed} m/s"
   
    
    await bot.send_message(message.chat.id, message_text, reply_markup=custom_keyboard)

@dp.message_handler(commands=["help"])
async def send_help(message: aiogram.types.Message):
    help_text = "This bot can show you the current weather in any location. To get started, type /start followed by the name of a city or town.\n\n"
    help_text += "Example: /start London"
    await bot.send_message(message.chat.id, help_text, reply_markup=custom_keyboard)

if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)