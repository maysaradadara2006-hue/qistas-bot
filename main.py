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
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0",
        })

        session.get(LOGIN_URL, timeout=60)

        session.post(LOGIN_URL, data={
            "username": USERNAME,
            "password": PASSWORD,
            "country": "1"
        }, timeout=60)

        r = session.get(TASKS_URL, timeout=60)

        if "لا يوجد لديك مهام" in r.text:
            send_telegram("❌ لا يوجد شغل حالياً")
        else:
            send_telegram("🎉 يوجد شغل!\nhttps://dms.qistas.com/dmz/datagathering/lawnews/autotasks")

    except Exception as e:
        send_telegram(f"⚠️ خطأ: {e}")

send_telegram("🤖 البوت شغال!")
schedule.every(15).minutes.do(check_and_notify)

check_and_notify()

while True:
    schedule.run_pending()
    time.sleep(30)
