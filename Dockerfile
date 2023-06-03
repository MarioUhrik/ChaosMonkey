FROM python:3.12-rc-alpine

WORKDIR /app

COPY src/* /app/

RUN pip3 install -r requirements.txt

CMD python3 /app/main.py
