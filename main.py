from gtts import gTTS
import telebot
from flask import Flask, request
import os

TOKEN = os.environ.get('TOKEN')


bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
print ("Bot Is Running....")

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi 👋, I am Text To Voice Bot, Send me a Text Massage and I will send you back mp3 Audio 🔉 of That Text message!\
""")

@bot.message_handler(content_types=['document','photo','video','voice','sticker','video_note','location','contact'])
def handle_docs_audio(message):
	bot.reply_to(message, "Send me Text Only!😶")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    tts = gTTS(message.text, lang='en',tld='co.in')
    tts.save('hello.mp3')
    path = './hello.mp3'
    file=open(path, "rb")
    # print (file)
    bot.send_message(message.chat.id, "Sending Audio File....")
    bot.send_document(message.chat.id,file)


@server.route('/' + TOKEN , methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://fast-rest-api.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

