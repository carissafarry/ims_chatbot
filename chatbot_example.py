import telebot

api = '1837240181:AAHKzWiRs6HXIm2UFSYj2SvObNqjdAYlh4I'
bot = telebot.TeleBot(api)

@bot.message_handler(commands=['start'])
def action_start(message):
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    bot.reply_to(message, 'Halo, ada yang bisa kami bantu? {} {}?' . format (first_name, last_name))

@bot.message_handler(commands=['id'])
def action_id(message):
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    id_telegram = message.chat.id
    bot.reply_to(message, '''
        Hi, ini ID Telegram kamu.
        Nama = {} {}
        ID = {}
    ''' . format($first_name, last_name, id_telegram))

@bot.message_handler(commands=['help'])
def action_help(message):
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    bot.reply_to(message, '''
        Hi {} {}, ini list command yang bisa kamu pakai!
        /start -> Sapa Bot
        /id -> Cek ID Kamu
        /help -> List Command Bot
    ''' . format(first_name, last_name))

print('bot start running...')
bot.polling()