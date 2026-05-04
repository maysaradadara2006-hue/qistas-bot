import time
import schedule
import requests

BOT_TOKEN = "8777724163:AAEPlhvjqyjvQ1HS3BfmkFkjCO-LE3Rylb8"
CHAT_ID = "5985354863"

LOGIN_URL = "https://dms.qistas.com/dmz/datagathering/lawnews/autotasks"
TASKS_URL = "https://dms.qistas.com/dmz/datagathering/lawnews/autotasks/get?"

USERNAME = "Maysarah"
PASSWORD = "1469"

def send_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=30
        )
    except:
        pass

def check_and_notify():
    try:
        send_telegram("🔄 جاري فحص قسطاس...")

        s = requests.Session()
        s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ar,en;q=0.9",
            "Connection": "keep-alive"
        })

        s.get(LOGIN_URL, timeout=90)

        s.post(
            LOGIN_URL,
            data={
                "username": USERNAME,
                "password": PASSWORD,
                "country": "1"
            },
            timeout=90
        )

        r = s.get(TASKS_URL, timeout=90)
        text = r.text

        if "لا يوجد لديك مهام" in text:
            send_telegram("❌ لا يوجد شغل حالياً في قسطاس")
        elif "تسجيل الدخول" in text:
            send_telegram("⚠️ لم يتم تسجيل الدخول. لازم نعرف اسم الحقول الصحيح.")
        else:
            send_telegram("🎉 يوجد شغل جديد!\nhttps://dms.qistas.com/dmz/datagathering/lawnews/autotasks")

    except requests.exceptions.ConnectTimeout:
        send_telegram("⚠️ Timeout: Railway مش قادر يوصل لموقع قسطاس.")
    except requests.exceptions.ReadTimeout:
        send_telegram("⚠️ الموقع تأخر بالرد. رح أجرب بعد 15 دقيقة.")
    except Exception as e:
        send_telegram(f"⚠️ خطأ:\n{e}")

send_telegram("🤖 البوت شغال! يتحقق كل 15 دقيقة.")
schedule.every(15).minutes.do(check_and_notify)

check_and_notify()

while True:
    schedule.run_pending()
    time.sleep(30)
