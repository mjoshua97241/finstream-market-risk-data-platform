FROM apache/airflow:3.1.0

USER airflow

COPY ../requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir \
    -r /requirements.txt \
    --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.12.txt