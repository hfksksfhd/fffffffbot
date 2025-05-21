import telebot
import requests
import re
from admin_panel import AdminPanel

TOKEN = "7982244762:AAGIFwICp3hP2nuJonkI3KO8IiiqqVZC6O4"
bot = telebot.TeleBot(TOKEN)
admin_panel = AdminPanel(bot)

API_URL = "https://dark.faresveno.workers.dev/?ask={}&model=1"

# دالة تنضيف الرد من الرموز والتنسيق
def clean_reply(text):
    text = text.replace("𓆑", "")
    text = text.replace("\\n", "\n").replace("\\", "")
    return text.strip()

# أمر البداية
@bot.message_handler(commands=['start'])
def start(message):
    admin_panel.add_user(message.from_user.id, message.from_user.username)
    bot.send_message(message.chat.id, "أهلاً بيك! ابعتلي سؤالك وأنا هرد عليك باستخدام الذكاء الاصطناعي.", parse_mode="Markdown")

# أمر لوحة الإدارة
@bot.message_handler(commands=['admin'])
def admin_command(message):
    admin_panel.handle_admin_command(message)

# استقبال ضغطات الأزرار من لوحة الإدارة
@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def handle_admin_callback(call):
    admin_panel.handle_admin_callback(call)

# استقبال أي رسالة (كسؤال للذكاء الاصطناعي)
@bot.message_handler(func=lambda m: True)
def ask_ai(message):
    user_id = message.from_user.id

    if admin_panel.is_banned(user_id):
        bot.send_message(message.chat.id, "❌ أنت محظور من استخدام البوت.")
        return

    if not admin_panel.bot_data.get('is_active', True):
        bot.send_message(message.chat.id, "⛔ البوت متوقف مؤقتاً من قبل الإدارة.")
        return

    admin_panel.add_user(user_id, message.from_user.username)
    admin_panel.notify_admins(message)

    # عدّاد رسائل اليوم
    today = str(message.date)[:10]
    messages_today = admin_panel.bot_data.setdefault('messages_today', {})
    messages_today[today] = messages_today.get(today, 0) + 1
    admin_panel.save_bot_data()

    try:
        response = requests.get(API_URL.format(message.text))
        reply_json = response.json()
        reply = clean_reply(reply_json.get("reply", "معرفتش أرد دلوقتي، جرب تاني."))
        bot.send_message(message.chat.id, reply, parse_mode="Markdown")
    except Exception as e:
        print("AI Error:", e)
        bot.send_message(message.chat.id, "❌ حصل خطأ، حاول تاني.")

# تشغيل البوت
print("البوت شغال ✅")
bot.infinity_polling()