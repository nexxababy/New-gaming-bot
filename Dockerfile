FROM python:3.11-slim

# Working directory
WORKDIR /app

# Best practices
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure data folder exists (for user database, JSON, etc.)
RUN mkdir -p /app/data || true

# Optional: Keep data persistent
VOLUME ["/app/data"]

# Healthcheck (optional, checks if bot is running)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD pgrep -f "python bot.py" || exit 1

# Start bot
CMD ["python", "bot.py"]
