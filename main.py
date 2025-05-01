from flask import Flask, request
import random, time
from datetime import datetime
import os
import requests

app = Flask(__name__)
otp_data = {}

BOT_TOKEN = os.environ.get("8116545078:AAG2By1R61Xy3aeFU9F3eyoL-CfbimEbgac")
CHAT_ID = os.environ.get("7025388109")  # Atur dari Telegram user/bot

@app.route('/')
def index():
    return "OTP Bot Aktif!"

@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    otp = str(random.randint(100000, 999999))
    now = datetime.now()
    otp_data['code'] = otp
    otp_data['time'] = time.time()

    # Kirim ke Telegram
    message = f"OTP kamu: {otp}\nLogin waktu: {now.strftime('%d/%m/%Y pukul %H:%M:%S')}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

    return {'status': 'OTP sent'}

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    code = data.get("otp")

    if not otp_data:
        return {'status': 'OTP not generated'}, 400
    if time.time() - otp_data['time'] > 900:
        return {'status': 'OTP expired'}, 400
    if otp_data['code'] != code:
        return {'status': 'Incorrect OTP'}, 400

    return {'status': 'Verified'}

if __name__ == '__main__':
    app.run()
