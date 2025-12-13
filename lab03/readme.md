# lab03 – Automating currency script with cron in Docker

## 1. Scop

În acest laborator folosesc scriptul din **lab02** (`currency_exchange_rate.py`)
și configurez rularea lui automată cu **cron** într-un container Docker.

## 2. Structura proiectului (lab03)

- `currency_exchange_rate.py` – scriptul Python moștenit din lab02, care:
  - primește valutele și data din argumentele liniei de comandă;
  - trimite request la Web API-ul de curs valutar;
  - salvează rezultatul în fișiere JSON în directorul `data/`;
  - tratează erorile și le scrie în `error.log`.
- `cronjob` – fișier cu task-urile cron:
  - **zilnic la 06:00** – MDL → EUR pentru *ziua precedentă*;
  - **săptămânal vineri la 17:00** – MDL → USD pentru data de *acum 7 zile*.
- `entrypoint.sh` – scriptul de start al containerului:
  - creează `/var/log/cron.log` și setează permisiunile;
  - copiază și instalează fișierul `cronjob` ca crontab;
  - afișează job-urile instalate (`crontab -l`);
  - pornește monitorizarea logului (`tail -f /var/log/cron.log`);
  - pornește serviciul `cron` în foreground.
- `Dockerfile` – imagine bazată pe `python:3.12-slim`:
  - instalează `cron` și biblioteca `requests`;
  - copiază `currency_exchange_rate.py`, `cronjob` și `entrypoint.sh` în container;
  - setează directorul de lucru `/app`;
  - configurează entrypoint-ul `/entrypoint.sh`.
- `docker-compose.yml` – definește serviciul `lab03-cron`:
  - construiește imaginea din `Dockerfile`;
  - pornește containerul `lab03_currency_cron`;
  - setează variabile de mediu:
    - `API_KEY=EXAMPLE_API_KEY`;
    - `CURRENCY_API_URL=http://host.docker.internal:8080/` (API-ul din lab02).

## 3. Cum pornesc API-ul de curs valutar (lab02prep)

1. Din rădăcina proiectului:

```bash
cd lab02prep
docker-compose up --build
```

Serviciul pornește în containerul `php_apache` și ascultă pe portul 8080.

Fereastra cu `docker-compose up` trebuie lăsată deschisă.

## 4. Cum construiesc și pornesc containerul cu cron (lab03)

Din directorul lab03:
```
cd lab03
docker-compose up --build
```
Aceasta:

construiește imaginea `lab03-lab03-cron` pe baza `Dockerfile`;

pornește containerul `lab03_currency_cron`;

în interior se execută `entrypoint.sh`, care:

creează `/var/log/cron.log`;

instalează job-urile cron din fișierul `cronjob`;

pornește serviciul `cron` și monitorizează logurile.

Output-ul tipic la start include:

```
Creating log file...

Log file created at /var/log/cron.log

=== Setting up cron jobs ===

Cron jobs installed: ...

=== Starting cron daemon ===

=== Monitoring cron logs ===
```

## 5. Verificarea executării task-urilor cron
5.1. Vizualizarea logurilor din container

Din afara containerului:
```
docker logs -f lab03_currency_cron
```

sau, dacă vreau să văd direct fișierul de log:
```
docker exec -it lab03_currency_cron sh
cat /var/log/cron.log
crontab -l
exit
```

În acest fișier se scriu:

mesajele de start ale entrypoint-ului;

rezultatele și/sau erorile generate de rularea scriptului
`currency_exchange_rate.py` la orele programate de cron.

5.2. Testarea manuală a scriptului în container

Pentru a verifica că scriptul comunică cu API-ul din lab02:
```
docker exec -it lab03_currency_cron sh
python /app/currency_exchange_rate.py MDL EUR 2025-01-01
exit
```

Dacă serverul API răspunde cu eroare (de exemplu HTTP 501), scriptul:

afișează mesajul în consolă;

salvează eroarea în fișierul de log, conform cerinței de tratare a erorilor.

## 6. Concluzie

În acest laborator am configurat un container Docker care rulează cron
și execută automat scriptul de schimb valutar la intervale prestabilite.
Am învățat să definesc task-uri cron într-un fișier separat, să pornesc
serviciul cron dintr-un script de entrypoint și să redirecționez output-ul
și erorile către un fișier de log `(/var/log/cron.log)`. Astfel,
automatizarea scriptului nu mai depinde de rularea manuală, ci este
gestionată de cron în interiorul containerului.

## Git: https://github.com/ArtemieJ/automation ##
