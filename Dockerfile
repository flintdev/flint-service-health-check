FROM python:3.7.7-alpine3.11
RUN pip install requests
COPY ./health_check.py /app/watcher.py