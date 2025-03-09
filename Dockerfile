FROM python:3.10-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get -y install \
    tesseract-ocr \
    tesseract-ocr-jpn \
    libgl1-mesa-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем код приложения
COPY . .

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip && \
    pip install \
    pillow \
    pytesseract \
    -r requirements.txt

# Запускаем приложение
CMD ["uvicorn", "second_dir.main:app", "--host", "0.0.0.0", "--port", "8000"]