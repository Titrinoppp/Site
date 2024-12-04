from flask import Flask, render_template, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)

def getKey():
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        )
    }
    url = "https://cgerrydlc.ru/Cherry/FREEMODS/LEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOoo56465465656546456rtrythghhgfh676765765767657657hjhgjghjghjghjhgjghjghj6786756756fgh1r.php"
    
    try:
        # Первый запрос для получения редиректа
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Проверяем статус ответа
        script = response.text
        redirect_url = script.replace("<script>setTimeout(function() { window.location.href='", '')\
                               .replace("'; }, 1);</script>", '')
        
        # Второй запрос для получения ключа
        response = requests.get(redirect_url, headers=headers, timeout=5)
        response.raise_for_status()
        key = response.text.split("- ")[1].strip()
        return key
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None
    except (IndexError, ValueError):
        print("Ошибка при обработке данных от сервера")
        return None

def generate_keys():
    with ThreadPoolExecutor(max_workers=10) as executor:
        keys = list(executor.map(lambda _: getKey(), range(1)))
    return [key for key in keys if key is not None]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_keys')
def generate_keys_route():
    start_time = time.time()
    keys = generate_keys()
    end_time = time.time()
    generation_time = end_time - start_time
    return jsonify(keys=keys, time=generation_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
