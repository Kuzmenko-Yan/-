import telebot
import requests
import sqlite3
from telebot import types

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)

DB = "weather.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        cities TEXT DEFAULT '[]'
    )""")
    conn.commit()
    conn.close()

init_db()

CITIES = {
    "Москва": (55.7558, 37.6173), "Санкт-Петербург": (59.9343, 30.3351),
    "Новосибирск": (55.0084, 82.9357), "Екатеринбург": (56.8389, 60.6057),
    "Казань": (55.7887, 49.1221), "Нижний Новгород": (56.3269, 44.0059),
    "Челябинск": (55.1644, 61.4368), "Самара": (53.1959, 50.1002),
    "Омск": (54.9885, 73.3242), "Ростов-на-Дону": (47.2357, 39.7015),
    "Уфа": (54.7388, 55.9721), "Красноярск": (56.0153, 92.8932),
    "Воронеж": (51.6720, 39.1843), "Пермь": (58.0105, 56.2502),
    "Волгоград": (48.7080, 44.5133), "Краснодар": (45.0355, 38.9753),
    "Саратов": (51.5336, 46.0343), "Тюмень": (57.1522, 65.5272),
    "Тольятти": (53.5078, 49.4204), "Ижевск": (56.8527, 53.2114),
    "Барнаул": (53.3467, 83.7836), "Ульяновск": (54.3142, 48.4031),
    "Иркутск": (52.2978, 104.2964), "Хабаровск": (48.4827, 135.0844),
    "Ярославль": (57.6261, 39.8845), "Владивосток": (43.1155, 131.8855),
    "Махачкала": (42.9849, 47.5047), "Томск": (56.4977, 84.9744),
    "Оренбург": (51.7727, 55.0988), "Кемерово": (55.3333, 86.0833),
    "Рязань": (54.6269, 39.6916), "Астрахань": (46.3497, 48.0408),
    "Пенза": (53.1959, 45.0183), "Липецк": (52.6031, 39.5708),
    "Киров": (58.6036, 49.6680), "Тула": (54.1961, 37.6182),
    "Калининград": (54.7104, 20.4522), "Брянск": (53.2434, 34.3656),
    "Курск": (51.7373, 36.1873), "Иваново": (56.9967, 40.9819),
    "Магнитогорск": (53.3922, 58.9801), "Тверь": (56.8587, 35.9176),
    "Ставрополь": (45.0428, 41.9734), "Белгород": (50.5955, 36.5878),
    "Архангельск": (64.5401, 40.5433), "Владимир": (56.1291, 40.4066),
    "Сочи": (43.5855, 39.7203), "Курган": (55.4415, 65.3410),
    "Смоленск": (54.7826, 32.0453), "Калуга": (54.5293, 36.2754),
    "Чита": (52.0340, 113.4994), "Орёл": (52.9651, 36.0693),
    "Волжский": (48.7854, 44.7759), "Череповец": (59.1269, 37.9090),
    "Вологда": (59.2181, 39.8886), "Саранск": (54.1838, 45.1749),
    "Тамбов": (52.7212, 41.4523), "Мурманск": (68.9585, 33.0827),
    "Петрозаводск": (61.7849, 34.3469), "Кострома": (57.7676, 40.9269),
    "Нижний Тагил": (57.9191, 59.9650), "Новороссийск": (44.7234, 37.7687),
}

WEATHER_CODES = {
    0: "☀️ Ясно", 1: "🌤 Преимущественно ясно", 2: "⛅ Переменная облачность",
    3: "️ Пасмурно", 45: "🌫 Туман", 48: "🌫 Иней", 51: "🌦 Лёгкая морось",
    53: " Морось", 55: " Сильная морось", 61: "🌧 Лёгкий дождь",
    63: "🌧 Дождь", 65: "🌧 Сильный дождь", 71: " Лёгкий снег",
    73: "🌨 Снег", 75: "❄️ Сильный снег", 80: "🌧 Ливень",
    81: " Сильный ливень", 82: "🌧 Ливень", 95: "⛈ Гроза",
    96: "⛈ Гроза с градом", 99: "⛈ Сильная гроза с градом"
}

def get_user_cities(user_id):
    conn = sqlite3.connect(DB)
    cur = conn.execute("SELECT cities FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return eval(row[0]) if row else []

def save_user_cities(user_id, cities):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT OR REPLACE INTO users (user_id, cities) VALUES (?, ?)",
                 (user_id, str(cities)))
    conn.commit()
    conn.close()

def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&windspeed_unit=ms"
    data = requests.get(url, timeout=5).json()
    cw = data["current_weather"]
    desc = WEATHER_CODES.get(cw["weathercode"], "")
    return f"{cw['temperature']}°C, {cw['windspeed']} м/с, {desc}"

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(" Поиск города", callback_data="search"))
    markup.add(types.InlineKeyboardButton("🌤 Моя погода", callback_data="my_weather"))
    bot.send_message(message.chat.id, "👋 Привет! Выбери действие:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "search")
def search_city(call):
    bot.send_message(call.message.chat.id, "🔍 Введи название города:")
    bot.register_next_step_handler(call.message, process_city_search)

def process_city_search(message):
    query = message.text.strip().lower()
    matches = [c for c in CITIES if query in c.lower()]
    if not matches:
        bot.send_message(message.chat.id, "❌ Город не найден. Попробуй ещё раз.")
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    for city in matches[:10]:
        markup.add(types.InlineKeyboardButton(city, callback_data=f"add_{city}"))
    bot.send_message(message.chat.id, f"📍 Найдено {len(matches)} городов. Выбери:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("add_"))
def add_city(call):
    city = call.data[4:]
    user_id = call.message.chat.id
    cities = get_user_cities(user_id)
    if city in cities:
        bot.answer_callback_query(call.id, "⚠️ Уже в списке!")
        return
    cities.append(city)
    save_user_cities(user_id, cities)
    bot.answer_callback_query(call.id, f"✅ {city} добавлен!")
    show_weather(call.message)

@bot.callback_query_handler(func=lambda c: c.data == "my_weather")
def my_weather(call):
    show_weather(call.message)

def show_weather(message):
    user_id = message.chat.id
    cities = get_user_cities(user_id)
    if not cities:
        bot.send_message(user_id, "📭 Список пуст. Добавь города через поиск.")
        return
    text = "🌤 **Твоя погода:**\n\n"
    markup = types.InlineKeyboardMarkup(row_width=1)
    for city in cities:
        lat, lon = CITIES[city]
        weather = get_weather(lat, lon)
        text += f"**{city}**: {weather}\n"
        markup.add(types.InlineKeyboardButton(f"❌ {city}", callback_data=f"remove_{city}"))
    markup.add(types.InlineKeyboardButton("➕ Добавить город", callback_data="search"))
    bot.send_message(user_id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("remove_"))
def remove_city(call):
    city = call.data[7:]
    user_id = call.message.chat.id
    cities = get_user_cities(user_id)
    if city in cities:
        cities.remove(city)
        save_user_cities(user_id, cities)
    bot.answer_callback_query(call.id, f" {city} удалён!")
    show_weather(call.message)

print("✅ Бот запущен!")
bot.polling()
