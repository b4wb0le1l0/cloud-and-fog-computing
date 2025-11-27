FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py \
    REDIS_HOST=redis \
    REDIS_PORT=6379

EXPOSE 5000

CMD ["python", "app.py"]