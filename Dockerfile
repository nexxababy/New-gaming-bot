# Dockerfile
FROM python:3.11-slim

WORKDIR /app
# keep pip cache small
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ensure data file exists and is writeable
RUN mkdir -p /app/data || true

CMD ["python", "bot.py"]
