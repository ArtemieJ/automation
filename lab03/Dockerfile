# Folosim imaginea oficială Python (Debian slim)
FROM python:3.12-slim

# Instalăm cron (pentru job-urile programate)
RUN apt-get update && \
    apt-get install -y cron && \
    rm -rf /var/lib/apt/lists/*

# Directorul de lucru în container
WORKDIR /app

# Copiem scriptul și fișierele necesare în container
COPY currency_exchange_rate.py /app/currency_exchange_rate.py
COPY cronjob /app/cronjob
COPY entrypoint.sh /entrypoint.sh

# Instalăm biblioteca necesară scriptului
RUN pip install --no-cache-dir requests

# Facem entrypoint-ul executabil
RUN chmod +x /entrypoint.sh

# La pornirea containerului se rulează entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
