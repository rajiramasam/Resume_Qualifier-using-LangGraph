FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

 EXPOSE 5000

 CMD ["python", "app.py"]