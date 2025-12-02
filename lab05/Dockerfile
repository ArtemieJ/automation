FROM jenkins/ssh-agent:latest

USER root
RUN apt-get update \
 && apt-get install -y php-cli php-xml php-mbstring unzip git curl \
 && rm -rf /var/lib/apt/lists/*

RUN curl -sS https://getcomposer.org/installer -o /tmp/installer.php \
 && php /tmp/installer.php --install-dir=/usr/local/bin --filename=composer \
 && rm /tmp/installer.php

USER jenkins
