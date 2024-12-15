FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONPATH="${PYTHONPATH}:/app/commands"
ENV PYTHONPATH="${PYTHONPATH}:/app/api"
ENV PYTHONPATH="${PYTHONPATH}:/app/db"

CMD ["python", "bot/main.py"]
