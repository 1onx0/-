import os
import yt_dlp
from telebot import TeleBot

# جلب التوكن من إعدادات السيرفر الآمنة (البيئة المحيطة)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def download_and_send_video(message):
    url = message.text
    if "http" in url:
        status_msg = bot.reply_to(message, "⏳ جاري جلب الفيديو والتحميل، انتظر قليلاً...")
        
        # إعدادات تحميل الفيديو بجودة مناسبة وتسمية الملف
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best',
            'no_warnings': True,
            'quiet': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            # إرسال الفيديو للمستخدم في تليجرام
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video, reply_to_message_id=message.message_id)
            
            # تنظيف السيرفر وحذف الملف فوراً لتوفير المساحة
            if os.path.exists(filename):
                os.remove(filename)
            bot.delete_message(message.chat.id, status_msg.message_id)
            
        except Exception as e:
            bot.edit_message_text(f"❌ حدث خطأ أثناء التحميل: {str(e)}", message.chat.id, status_msg.message_id)
            if 'filename' in locals() and os.path.exists(filename):
                os.remove(filename)
    else:
        bot.reply_to(message, "يرجى إرسال رابط فيديو صحيح.")

# تشغيل البوت بشكل مستمر
if __name__ == "__main__":
    print("البوت يعمل الآن...")
    bot.infinity_polling()
