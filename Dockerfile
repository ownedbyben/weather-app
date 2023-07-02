FROM python:3.9-alpine

WORKDIR /app

COPY requirment.txt .

RUN pip install --upgrade pip
RUN pip install -r requirment.txt

COPY . .


CMD gunicorn -w 3 --bind 0.0.0.0:5000 project:app --log-level debug
