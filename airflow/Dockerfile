FROM apache/airflow:3.1.0

USER root

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && apt-get clean

USER airflow

COPY ../requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt