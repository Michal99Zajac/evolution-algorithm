FROM python:3.11.0-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /src .

ENV PORT 8080

EXPOSE ${PORT}

CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1 --reload
