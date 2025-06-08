FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./app ./app

EXPOSE 5000

# explicitly include /app in PYTHONPATH
ENV PYTHONPATH=/app

CMD ["python", "app/main.py"]
