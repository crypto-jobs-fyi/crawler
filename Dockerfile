FROM python:3.12-slim

WORKDIR /data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m playwright install --with-deps chromium

COPY . .

CMD ["python3", "crawler_ai.py"]
