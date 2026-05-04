import time, schedule, requests

BOT_TOKEN = "8777724163:AAFCJG5eMeS8JnqBIFRP1a9W3-s80XuPAvE"
CHAT_ID = "5985354863"
LOGIN_URL = "https://dms.qistas.com/dmz/datagathering/lawnews/autotasks"
TASKS_URL = "https://dms.qistas.com/dmz/datagathering/lawnews/autotasks/get?"
USERNAME = "Maysarah"
PASSWORD = "1469"

def send_telegram(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}, timeout=10)

def check_and_notify():
    try:
        s = requests.Session()
        s.headers.update({"User-Agent": "Mozilla/5.0"})
        s.get(LOGIN_URL, timeout=15)
        s.post(LOGIN_URL, data={"username": USERNAME, "password": PASSWORD, "country": "1"}, timeout=15)
        r = s.get(TASKS_URL, timeout=15)
        if "لا يوجد لديك مهام" in r.text:
            send_telegram("لا يوجد شغل حالياً في قسطاس")
        else:
            send_telegram("يوجد شغل جديد!\nhttps://dms.qistas.com/dmz/datagathering/lawnews/autotasks")
    except Exception as e:
        send_telegram(f"خطا: {e}")

send_telegram("البوت شغال! يتحقق كل 15 دقيقة")
schedule.every(15).minutes.do(check_and_notify)
check_and_notify()
while True:
    schedule.run_pending()
    time.sleep(30)
