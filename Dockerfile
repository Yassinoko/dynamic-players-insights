FROM python:3.10.6-buster

COPY requirements.txt requirements.txt
COPY playerprediction playerprediction
COPY setup.py setup.py

RUN pip install .
RUN pip install --upgrade pip

WORKDIR /app

CMD uvicorn main.api.fast:app --host 0.0.0.0 --port 8080
