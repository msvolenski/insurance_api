# Dockerfile for Insurance API Service

FROM python:3.8.3-alpine3.12
LABEL author="Matheus Smythe Svolenski"

WORKDIR /app
EXPOSE 5000

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY entrypoint.sh /app/
COPY *.py /app/
COPY application /app/application/
COPY migrations /app/migrations/

ENTRYPOINT ["./entrypoint.sh"]
