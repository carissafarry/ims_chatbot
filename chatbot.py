import telebot
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '',
    database = 'ims_naila'
)

# cek database apakah sudah connect
# print(mydb)

# input ke sql
sql = mydb.cursor()

# with mydb.cursor () as cursor:
#     sql = "query" 
#     cursor.execute (sql)
#     mydb.commit ()
#     mydb.close ()

api = '1837240181:AAHKzWiRs6HXIm2UFSYj2SvObNqjdAYlh4I'
bot = telebot.TeleBot(api)
cart = [[]]

@bot.message_handler(commands=['user'])
def action_user(message):
    print(message.chat)


@bot.message_handler(commands=['daftar'])
def action_daftar(message):
    texts = message.text.split(' ')
    nama = message.chat.first_name + ' ' + message.chat.last_name
    username = message.chat.username
    alamat = texts[1]
    admin = 0

    insert = "insert into user(admin, nama, username, alamat) values (%d, %s, %s, %s)"
    val = (admin, nama, username, alamat)
    sql.execute(insert, val)
    mydb.commit()

    # with mydb.cursor () as cursor:
    #     insert = "insert into user(admin, nama, username, alamat) values (%d, %s, %s, %s)" 
    #     val = (admin, nama, username, alamat)
    #     cursor.execute (insert, val)
    #     mydb.commit ()
    #     mydb.close ()

    bot.reply_to(message, "Selamat {}, Anda sudah terdaftar! Silahkan berbelanja!" . format(nama))


@bot.message_handler(commands=['toko'])
def action_toko(message):
    # splie pesan dari input user
    texts = message.text.split(' ')
    # print(texts)

    # tampilkan data toko
    sql.execute("select nama_toko from toko")
    toko = sql.fetchall()

    # penomoran
    num = 0

    # pesan reply dari bot
    reply = ''
    for x in toko:
        num = num + 1
        reply = reply + str(num) + '. ' + str(x) + '\n'
    
    # hilangkan karakter tidak perlu
    reply = reply.replace("'", "")
    reply = reply.replace("(", "")
    reply = reply.replace(")", "")
    reply = reply.replace(",", "")

    bot.reply_to(message, reply)


@bot.message_handler(commands=['produk'])
def action_produk(message):
    texts = message.text.split(' ')
    pilihan = texts[1]

    if pilihan != None :
        sql.execute("select nama from produk where id_toko='{}'" . format(pilihan))
        output = sql.fetchall()

    num = 0

    reply = ''
    for x in output:
        num = num + 1
        reply = reply + str(num) + '. ' + str(x) + '\n'

    reply = reply.replace("'", "")
    reply = reply.replace("(", "")
    reply = reply.replace(")", "")
    reply = reply.replace(",", "")

    bot.reply_to(message, reply)


@bot.message_handler(commands=['cart'])
def action_cart(message):
    texts = message.text.split(' ')

    toko = texts[1]
    produk = texts[2]
    jumlah = texts[3]
    a = []

    if cart[0] == [] :
        cart[0].append(toko)
        cart[0].append(produk)
        cart[0].append(jumlah)
    else :
        detail = []
        detail.append(toko)
        detail.append(produk)
        detail.append(jumlah)
        cart.append(detail)

    num = 0

    reply = ''
    for x in range(0, len(cart)):
        num = num + 1
        reply = reply + str(num) + '. Toko        : ' + str(cart[x][0]) + '\n' 
        reply = reply + '     Produk   : ' + str(cart[x][1]) + '\n'
        reply = reply + '     Jumlah  : ' + str(cart[x][2]) + '\n\n'

    caption = '***   Keranjang Anda :   ***' + '\n'
    botReply = caption + reply
    bot.reply_to(message, botReply)


@bot.message_handler(commands=['beli'])
def action_beli(message):
    getUserData = "select id, username from user where username='{}'" . format(message.chat.username)
    sql.execute(getUserData)
    userData = sql.fetchone()
    nama = message.chat.first_name

    if userData is None :
        bot.reply_to(message, '''Hai {}! Mohon mendaftarkan akun Anda terlebih dahulu, dengan mengetik "/daftar <alamat_anda>"''' . format(nama))
    else :
        id_user = userData.id
        dateTimeObj = datetime.now()
        waktu = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

        for x in range(0, len(cart)):
            id_toko = cart[x][0]
            insert = "insert into orders(id_toko, id_user, waktu) values (%d, %d, %s)"
            val = (id_toko, id_user, waktu)
            sql.execute(insert, val)
            mydb.commit()

            # with mydb.cursor () as cursor :
            #     insert = "insert into orders(id_toko, id_user, waktu) values (%d, %d, %s)" 
            #     val = (id_toko, id_user, waktu)
            #     cursor.execute (insert, val)
            #     mydb.commit ()
            #     mydb.close ()

    reply = "Terima kasih " + nama + " sudah membeli melalui chatbot kami!" + "\n\n" + "Silakan melakukan pembayaran dengan mengirimkan nota dengan nominal Rp XXX melalui:" + "\n\n" + "Bank Mandiri" + "\n" + "1710005251254" + "\n" + "a.n. Carissa Farry"
    bot.reply_to(message, reply)


print('bot start running...')
bot.polling()