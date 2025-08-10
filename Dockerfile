FROM python:3.8-slim-buster
WORKDIR /app
COPY . /app

RUN apt-get update -y && \
    apt-get install -y ffmpeg libsm6 libxext6 unzip awscli apt-transport-https ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]