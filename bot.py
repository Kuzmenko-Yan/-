import telebot
import requests

# Замени на свой токен от @BotFather
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
# Замени на свой ключ от https://openweathermap.org/api
WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"

bot = telebot.TeleBot(BOT_TOKEN)

def get_weather():
    city = "Vladivostok"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url).json()
        if response.get("cod") == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            wind = response["wind"]["speed"]
            return f" Владивосток\n🌡 Температура: {temp}°C\n💨 Ветер: {wind} м/с\n {desc.capitalize()}"
        return "❌ Не удалось получить погоду"
    except Exception:
        return "❌ Ошибка подключения"

@bot.message_handler(commands=["start", "weather"])
def send_weather(message):
    bot.reply_to(message, get_weather())

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, get_weather())

print("✅ Бот запущен!")
bot.polling()
