# Lab01 — backup.sh

Script Shell pentru backup rapid (arhivă `tar.gz`) al unui director.

## Ce face
- Creează fișier `tar.gz` al directorului sursă.
- Numele include data/ora: `<nume_sursa>_YYYY-MM-DD_HH-MM-SS.tar.gz`.
- Verifică existența și permisiunile directoarelor.

## Utilizare
./backup.sh <source_dir> [destination_dir=/backup]

- `<source_dir>` — obligatoriu.
- `[destination_dir]` — opțional, implicit `/backup`.

> Notă: Scriptul NU creează automat directorul de destinație; trebuie să existe și să fie inscriptibil.

## Exemple
# Backup în HOME (recomandat pe Git Bash, Windows)
mkdir -p "$HOME/backups"
./backup.sh /tmp/demo/src "$HOME/backups"

# Linux nativ (exemplu cu /backup implicit):
# sudo mkdir -p /backup && sudo chown "$USER":"$USER" /backup
# ./backup.sh /etc

## Coduri de ieșire
0 succes; 2 utilizare incorectă; 3 sursă inexistentă;
4 destinație inexistentă; 5 fără permisiune; 6 arhiva nu a fost creată

## Dependențe
tar, coreutils (date/stat)
