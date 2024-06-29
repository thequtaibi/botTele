import datetime
import pytz
from telegram import Bot
from time import sleep

# تعريف معلومات التواصل مع التليجرام
TOKEN = '7383336156:AAFeNRBYf-3f5GmvUpWbNioe3AbLdU8Wv8I'  # قم بوضع توكن البوت الخاص بك هنا
CHAT_ID = -1002215256958  # قم بوضع ID الشات هنا

# إعداد التوقيت لمدينة الرياض
riyadh = pytz.timezone('Asia/Riyadh')

# إعداد البوت
bot = Bot(token=TOKEN)

# دالة لإرسال الرسالة المحددة
def send_message():
    message = "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا باللَّهِ الْعَلِيُّ الْعَظِيم"
    bot.send_chat_action(chat_id=CHAT_ID, action='typing')
    sleep(2)  # انتظر لعرض حالة الكتابة
    bot.send_message(chat_id=CHAT_ID, text=message)

# دالة تشغيل البوت
def main():
    while True:
        now = datetime.datetime.now()
        # تحويل التوقيت إلى التوقيت الصحيح
        now = pytz.utc.localize(now).astimezone(riyadh)
        
        # إذا كان التوقيت حاليًا 00 دقيقة من كل ساعة
        if now.minute == 0:
            send_message()  # أرسل الرسالة الآن

        # الساعة التالية
        next_hour = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
        delta = next_hour - now
        # انتظر لحين الوصول إلى الساعة التالية
        sleep(delta.seconds)

if __name__ == '__main__':
    main()
