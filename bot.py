import telebot
import requests

# Замени на свой токен от @BotFather
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

bot = telebot.TeleBot(BOT_TOKEN)

# Координаты Владивостока
LAT, LON = 43.1155, 131.8855

def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true&windspeed_unit=ms"
    try:
        data = requests.get(url).json()
        temp = data["current_weather"]["temperature"]
        wind = data["current_weather"]["windspeed"]
        code = data["current_weather"]["weathercode"]
        
        weather_desc = {
            0: "☀️ Ясно", 1: " Преимущественно ясно", 2: "⛅ Переменная облачность",
            3: "☁️ Пасмурно", 45: "🌫 Туман", 48: "🌫 Иней", 51: " Лёгкая морось",
            53: "🌦 Морось", 55: "🌧 Сильная морось", 61: "🌧 Лёгкий дождь",
            63: "🌧 Дождь", 65: "🌧 Сильный дождь", 71: "🌨 Лёгкий снег",
            73: "🌨 Снег", 75: "❄️ Сильный снег", 80: "🌧 Ливень",
            81: "🌧 Сильный ливень", 82: " Ливень", 95: "⛈ Гроза",
            96: "⛈ Гроза с градом", 99: "⛈ Сильная гроза с градом"
        }
        desc = weather_desc.get(code, " Неизвестно")
        
        return f"📍 Владивосток\n Температура: {temp}°C\n Ветер: {wind} м/с\n{desc}"
    except Exception:
        return "❌ Не удалось получить погоду"

@bot.message_handler(commands=["start", "weather"])
def send_weather(message):
    bot.reply_to(message, get_weather())

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, get_weather())

print("✅ Бот запущен!")
bot.polling()
