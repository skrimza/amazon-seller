FROM python:3.11.5-alpine3.18

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создание директорий для статических файлов
RUN mkdir -p /app/static/css
RUN mkdir -p /app/static/images
RUN mkdir -p /app/static/js

# Копирование статических файлов
COPY static/css /app/static/css
COPY static/images /app/static/images
COPY static/js /app/static/js

# Копирование шаблонов
COPY templates /app/templates

# Установка переменных окружения
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Установка прав доступа
RUN chmod -R 755 /app

EXPOSE 8000

# Запуск приложения
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]