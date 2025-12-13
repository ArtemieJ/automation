\# lab02 – Currency exchange rate script



\## 1. Requirements



\- Python 3

\- Biblioteca `requests`

\- Serviciul de curs valutar din proiectul `lab02prep` pornit local (Docker)



Instalarea dependențelor:



```

pip install requests

```

\## 2. Pornirea serviciului API



Descărcați proiectul de suport lab02prep.



În directorul proiectului lab02prep creați fișierul .env:



```

copy sample.env .env

```

Porniți serviciul:

```

docker-compose up --build

```

Serviciul va fi disponibil la http://localhost:8080.

\## 3. Cum se rulează scriptul



Din root-ul proiectului de automation:

```

py lab02\\currency\_exchange\_rate.py USD EUR 2025-01-01

```



Argumente:



`from\_currency` – moneda sursă (ex: USD, EUR, MDL);



`to\_currency` – moneda destinație;



`date – data` în format `YYYY-MM-DD` (în intervalul 2025-01-01 – 2025-09-15).



Exemple:

```

py lab02\\currency\_exchange\_rate.py USD EUR 2025-01-01

py lab02\\currency\_exchange\_rate.py USD EUR 2025-03-01

py lab02\\currency\_exchange\_rate.py USD EUR 2025-05-01

py lab02\\currency\_exchange\_rate.py USD EUR 2025-07-01

py lab02\\currency\_exchange\_rate.py USD EUR 2025-09-01

```



Rezultatul:



datele primite se salvează în directorul `data/` (automat creat în root) sub formă de fișiere:

`rate\_FROM\_TO\_DATE.json`



erorile se afișează în consolă și se salvează în `error.log` în root-ul proiectului.

\## 4. Structura scriptului



Scriptul `lab02/currency\_exchange\_rate.py` este organizat astfel:



`parse\_args()` – citește monedele și data din linia de comandă.



`validate\_date(date\_str)` – verifică formatul datei YYYY-MM-DD.



`get\_project\_root()` – determină root-ul proiectului (părintele directorului lab02).



`ensure\_data\_dir(root)` – creează directorul data în root dacă nu există.



`log\_error(root, message)` – salvează mesajele de eroare în error.log.



`fetch\_exchange\_rate(from\_currency, to\_currency, date\_str)`:



trimite un request POST la `http://localhost:8080/` cu:



parametri GET: `from`, `to`, `date`



parametru POST: `key` (API key)



verifică codul HTTP, JSON-ul și câmpul error din răspuns;



întoarce câmpul data (monedele, rata, data).



`main()`:



citește argumentele;



validează data;



apelează API-ul;



salvează răspunsul în fișier JSON în data/;



afișează un rezumat în consolă.



\## Scriptul folosește variabila de mediu API\_KEY (dacă este setată) sau

valoarea implicită EXAMPLE\_API\_KEY, aceeași cu cea din .env al proiectului lab02prep.

\## Concluzie ##

La acest laborator am învățat să lucrez cu un Web API dintr-un script Python. Am pornit serviciul local cu Docker, am folosit o cheie API și am scris un script care primește din linia de comandă monedele și data, trimite cererea la server și salvează răspunsul în fișiere JSON. În plus, am tratat și erorile: dacă ceva nu merge (parametri greșiți, dată invalidă etc.), scriptul afișează un mesaj clar și scrie detaliile în fișierul error.log. Astfel, am exersat atât lucrul cu API-uri, cât și lucrul cu fișiere și gestionarea erorilor într-un mic script de automatizare.

## Git: https://github.com/ArtemieJ/automation/blob/lab02/README.md
