FROM python:3.13.12-slim-trixie

#RUN apt-get update \
#    && apt-get install -y --no-install-recommends --no-install-suggests \
#    build-essential default-libmysqlclient-dev \
#    && pip install --no-cache-dir --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY  . .

EXPOSE 5000

CMD ["python3", "server.py"]
