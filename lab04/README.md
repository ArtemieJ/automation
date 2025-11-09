# Lucrarea de laborator №4 – Jenkins CI/CD cu Agent SSH (PHP + PHPUnit)

## Scopul lucrării
Scopul lucrării este configurarea unui sistem de integrare continuă (CI) folosind Jenkins, unde build-urile și testele unei aplicații PHP sunt executate automat pe un agent SSH din Docker. Jenkins va descărca codul sursă dintr-un repository GitHub, va instala dependențele necesare și va rula testele unitare definite în proiect.

## Sarcina
Configurarea unui mediu Jenkins cu două containere Docker:
- **jenkins-controller** – containerul principal ce rulează serverul Jenkins.
- **ssh-agent** – containerul secundar care execută taskurile prin SSH.

Pipeline-ul trebuie să descarce codul, să instaleze dependențele PHP și să ruleze testele automat, afișând rezultatul în interfața Jenkins.

## Efectuarea lucrării

1. A fost creat directorul `lab04` și structura proiectului:
lab04/
├─ docker-compose.yml
├─ Dockerfile
├─ .env
├─ secrets/
│ ├─ jenkins_agent_ssh_key
│ ├─ jenkins_agent_ssh_key.pub
│ └─ .gitkeep
├─ php-app/
│ ├─ index.php
│ └─ composer.json
├─ tests/
│ └─ AddTest.php
└─ Jenkinsfile

2. A fost generată o pereche de chei SSH pentru conectarea agentului:
ssh-keygen -t ed25519 -f lab04/secrets/jenkins_agent_ssh_key -C "jenkins@agent" -N ""
3. A fost creat fișierul `.env` cu variabila:
JENKINS_AGENT_SSH_PUBKEY=ssh-ed25519 AAAAC3... jenkins@agent


4. A fost pornit Jenkins Controller cu comanda:
docker compose up -d --build

Accesul s-a făcut la adresa: http://localhost:8080

5. În interfața Jenkins s-au instalat pluginurile recomandate și s-a creat primul utilizator.

6. În secțiunea **Manage Credentials** a fost adăugat un credential de tip “SSH Username with private key” cu ID-ul `jenkins-ssh-agent-key` și username-ul `jenkins`.

7. A fost creat un nod nou:
- Nume: `ssh-agent1`
- Root directory: `/home/jenkins/agent`
- Launch method: SSH către `ssh-agent`
- Credential: `jenkins-ssh-agent-key`
- Label: `php-agent`

8. A fost creat fișierul `php-app/index.php`:
```php
<?php
echo "Hello! 2+3=" . (2 + 3);
A fost definit fișierul php-app/composer.json:


{
  "require": {},
  "require-dev": {
    "phpunit/phpunit": "^10.0"
  }
}
A fost adăugat testul tests/AddTest.php:


<?php
use PHPUnit\Framework\TestCase;

require_once __DIR__ . '/../php-app/index.php';

class AddTest extends TestCase {
    public function testAddition() {
        $this->assertEquals(5, 2 + 3);
    }
}
A fost creat fișierul Jenkinsfile:

pipeline {
  agent { label 'php-agent' }

  stages {
    stage('Install Dependencies') {
      steps {
        dir('lab04/php-app') {
          sh 'composer install --no-interaction --prefer-dist'
        }
      }
    }

    stage('Test') {
      steps {
        sh 'lab04/php-app/vendor/bin/phpunit --testdox lab04/tests'
      }
    }
  }

  post {
    always { echo 'Pipeline completed.' }
    success { echo 'All stages completed successfully!' }
    failure { echo 'Errors detected in the pipeline.' }
  }
}
A fost creat un job Jenkins de tip Pipeline from SCM, configurat cu:

Repository: https://github.com/ArtemieJ/automation

Branch: lab01

Script path: lab04/Jenkinsfile

După rularea pipeline-ului, rezultatul a fost:

Hello! 2+3=5
PHPUnit 10.5.58 by Sebastian Bergmann and contributors.
OK (1 test, 1 assertion)
Fișierul .gitignore:


php-app/vendor/
secrets/*
!secrets/.gitkeep
!secrets/jenkins_agent_ssh_key.pub
.env

Întrebări
1. Care este rolul agentului SSH în Jenkins?
Agentul rulează build-urile și testele la distanță, separând execuția de serverul principal Jenkins.

2. De ce este util un pipeline declarativ?
Pentru că permite definirea clară și automată a etapelor de build și test direct în codul sursă, menținând proiectul complet automatizat.

3. Ce avantaje oferă Jenkins în automatizarea CI/CD?
Permite rularea automată a testelor, buildurilor și deploy-urilor, gestionarea mai multor agenți și integrarea ușoară cu GitHub și Docker.

Concluzie
În cadrul lucrării am configurat un sistem complet Jenkins CI/CD, format dintr-un controller și un agent SSH. S-au rulat automat etapele de instalare a dependențelor și testare pentru o aplicație PHP, iar pipeline-ul s-a finalizat cu succes. Am învățat să configurez Jenkins, să definesc un pipeline declarativ și să utilizez containere Docker pentru rularea automată a testelor.