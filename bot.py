import telebot
from telebot import types
from covid import Covid
import time

covid = Covid()
bot = telebot.TeleBot("token")
input_text = "Choose country from this list or write it!"
all_countries_with_id = covid.list_countries()
all_countries = []
all_countries_lower = []

for c in all_countries_with_id:
	all_countries.append(c['name'])
	all_countries_lower.append(c['name'].lower())

def top(n=20):
	ans = f"<u>Top {n} countries (confirmed / deaths)</u>\n\n"
	for i in range(n):
		country = all_countries_lower[i]
		ans += f"{i + 1}) <b>{all_countries[i]}</b>: {covid.get_status_by_country_name(country)['confirmed']} / {covid.get_status_by_country_name(country)['deaths']}\n"
	return ans


def check_country(country):
	return country in all_countries_lower


def last_update(seconds):
	return time.gmtime(seconds/1000)

def check(t):
	ans = ""
	if t < 10:
		ans += str(0) + str(t)
	else:
		ans += str(t)
	return ans

def date(country):
	info = covid.get_status_by_country_name(country)['last_update']
	info = last_update(info)
	ans = ""
	ans += check(info[2]) + '-' + check(info[1]) + '-' + check(info[0]) + " "
	ans += check(info[3])+ ':' + check(info[4]) + ':' + check(info[5])
	return ans

def statistic(country):
	if country == 'us':
		ans = f"<u>COVID-19 information in <b>US</b>:</u>\n\n" \
		f"<b>Number of deaths: {covid.get_status_by_country_name(country)['deaths']}</b>\n" \
		f"<b>Number of confirmed: {covid.get_status_by_country_name(country)['confirmed']}</b>\n" \
		f"<b>Number of recovered: {covid.get_status_by_country_name(country)['recovered']}</b>\n" \
		f"<b>Last update date: {date(country)}</b>\n"
	else:
		ans = f"<u>COVID-19 information in <b>{country.title()}</b>:</u>\n\n" \
		f"<b>Number of deaths: {covid.get_status_by_country_name(country)['deaths']}</b>\n" \
		f"<b>Number of confirmed: {covid.get_status_by_country_name(country)['confirmed']}</b>\n" \
		f"<b>Number of recovered: {covid.get_status_by_country_name(country)['recovered']}</b>\n" \
		f"<b>Last update date: {date(country)}</b>\n"

	return ans

def all():
	ans = f"<u><b>Total</b> COVID-19 information:</u>\n\n" \
		f"<b>Number of deaths: {covid.get_total_deaths()}</b>\n" \
		f"<b>Number of confirmed: {covid.get_total_confirmed_cases()}</b>\n" \
		f"<b>Number of recovered: {covid.get_total_recovered()}</b>\n" 
	return ans


@bot.message_handler(commands=["countries"])
def list_info(message):
	ans = "List of all avaliable countries:\n"
	for i in range(len(all_countries)):
		ans += str(i + 1) + ") " +all_countries[i] + "\n"
	bot.send_message(message.chat.id, ans)


@bot.message_handler(commands=["start"])
def start(message):
	markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
	btn1 = types.KeyboardButton(text="Total")
	btn2 = types.KeyboardButton(text="Europe")
	btn3 = types.KeyboardButton(text="Asia")
	btn4 = types.KeyboardButton(text="North America")
	btn5 = types.KeyboardButton(text="Top 20")
	markup.row(btn2, btn3, btn4)
	markup.row(btn1, btn5)

	send_message = f"<b>Hello, {message.from_user.first_name}!</b> If you want to know statistics about COVID-19 " \
		f"write name of the country or use menu below!"
	bot.send_message(message.chat.id, send_message, parse_mode="html", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def mess(message):
	country = message.text.strip().lower()
	if country == "total":
		bot.send_message(message.chat.id, all(), parse_mode='html')
	elif country == "europe":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn1 = types.KeyboardButton(text="\U0001f1ee\U0001f1f9 Italy")
		btn2 = types.KeyboardButton(text="\U0001f1ea\U0001f1f8 Spain")
		btn3 = types.KeyboardButton(text="\U0001f1e9\U0001f1ea Germany")
		btn4 = types.KeyboardButton(text="\U0001f1f7\U0001f1fa Russia")
		btn5 = types.KeyboardButton(text="\U0001f1e7\U0001f1fe Belarus")
		btn6 = types.KeyboardButton(text="\U0001f1eb\U0001f1f7 France")
		btn7 = types.KeyboardButton(text="\u2b05\ufe0f Back to the start")
		keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
		bot.send_message(message.chat.id, input_text, reply_markup= keyboard)
	elif country == "us" or country == "usa":
		final_message = statistic('us')
		bot.send_message(message.chat.id, final_message, parse_mode='html')
	elif country == "top 20":
		bot.send_message(message.chat.id, top(20), parse_mode='html')
	elif country == "asia":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn1 = types.KeyboardButton(text="\U0001f1e8\U0001f1f3 China")
		btn2 = types.KeyboardButton(text="\U0001f1ef\U0001f1f5 Japan")
		btn3 = types.KeyboardButton(text="\U0001f1ee\U0001f1f3 India")
		btn4 = types.KeyboardButton(text="\u2b05\ufe0f Back to the start")
		keyboard.row(btn1, btn2, btn3)
		keyboard.row(btn4)
		bot.send_message(message.chat.id, input_text, reply_markup= keyboard)
	elif country == "north america":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn1 = types.KeyboardButton(text="\U0001f1fa\U0001f1f8 US")
		btn2 = types.KeyboardButton(text="\U0001f1e8\U0001f1e6 Canada")
		btn3 = types.KeyboardButton(text="\u2b05\ufe0f Back to the start")
		keyboard.row(btn1, btn2)
		keyboard.row(btn3)
		bot.send_message(message.chat.id, input_text, reply_markup= keyboard)
	elif country == '\u2b05\ufe0f back to the start':
		markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
		btn1 = types.KeyboardButton(text="Total")
		btn2 = types.KeyboardButton(text="Europe")
		btn3 = types.KeyboardButton(text="Asia")
		btn4 = types.KeyboardButton(text="North America")
		btn5 = types.KeyboardButton(text="Top 20")
		markup.row(btn2, btn3, btn4)
		markup.row(btn1, btn5)
		bot.send_message(message.chat.id, "Choose country from menu or write it!", reply_markup=markup)
	else:
		if check_country(country):
			final_message = statistic(country)
			bot.send_message(message.chat.id, final_message, parse_mode='html')
		else:
			country = ' '.join(country.split()[1:])
			if check_country(country):
				final_message = statistic(country)
				bot.send_message(message.chat.id, final_message, parse_mode='html')
			else:
				final_message = "Sorry, but this country is not in my list. \nYou can see list of all countries using /countries"
				bot.send_message(message.chat.id, final_message)

bot.infinity_polling(none_stop=True)
