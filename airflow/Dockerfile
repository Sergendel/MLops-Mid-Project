FROM apache/airflow:latest-python3.11

USER airflow

# Copy and install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt
