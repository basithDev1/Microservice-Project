FROM python:3.10-slim-bullseye

RUN apt-get update \ 
    && apt-get install -y --no-install-recommends --no-install-suggests\
    build-essential ffmpeg\
    pkg-config \
    gcc \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirement.txt /app
RUN pip install --no-cache-dir --requirement /app/requirement.txt
COPY . /app

CMD ["python3","consumer.py"]
