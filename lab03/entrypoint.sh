#!/bin/sh

create_log_file() {
    echo "Creating log file..."
    touch /var/log/cron.log
    chmod 666 /var/log/cron.log
    echo "Log file created at /var/log/cron.log"
}

setup_cron() {
    echo "=== Setting up cron jobs ==="
    # Copiem crontab-ul nostru în /etc/cron.d
    cp /app/cronjob /etc/cron.d/currency_cron
    chmod 0644 /etc/cron.d/currency_cron
    # Încărcăm cronjob-urile
    crontab /etc/cron.d/currency_cron
    echo "Cron jobs installed:"
    crontab -l
}

monitor_logs() {
    echo "=== Monitoring cron logs ==="
    tail -f /var/log/cron.log
}

run_cron() {
    echo "=== Starting cron daemon ==="
    exec cron -f
}

# Exportăm variabilele de mediu pentru cron
env > /etc/environment

create_log_file
setup_cron
monitor_logs &   # rulează în background
run_cron         # ține containerul pornit
