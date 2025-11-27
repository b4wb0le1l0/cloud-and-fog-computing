import os
import time
from flask import Flask, render_template_string
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


HTML_TEMPLATE = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #2d2d2d;
            padding: 30px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        .metric {
            margin: 25px 0;
            padding: 15px;
            background: #3d3d3d;
            border-radius: 5px;
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: #4CAF50;
            margin: 10px 0;
        }
        .metric-label {
            font-size: 14px;
            color: #aaa;
            text-transform: uppercase;
        }
        .timestamp {
            font-size: 12px;
            color: #666;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Системный монитор</h2>
        
        <div class="metric">
            <div class="metric-label">Всего запросов</div>
            <div class="metric-value">{{ request_count }}</div>
        </div>
        
        <div class="metric">
            <div class="metric-label">Время работы</div>
            <div class="metric-value">{{ uptime }} сек</div>
        </div>
        
        <div class="timestamp">
            Данные обновлены: {{ current_time }}
        </div>
    </div>
</body>
</html>
"""

start_time = time.time()

@app.route("/")
def index():
    try:
        request_count = redis_client.incr("request_count")
        
        uptime = int(time.time() - start_time)
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        return render_template_string(
            HTML_TEMPLATE, 
            request_count=request_count,
            uptime=uptime,
            current_time=current_time
        )
    except redis.exceptions.RedisError as e:
        return f"Ошибка подключения к хранилищу: {str(e)}", 500

@app.route("/health")
def health():
    """Простой эндпоинт для проверки"""
    return "OK"

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", os.getenv("PORT", 5000)))
    app.run(host=host, port=port)