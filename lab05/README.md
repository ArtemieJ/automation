# Lucrarea de laborator 5  
## Automatizare CI/CD cu Jenkins, Docker și Ansible (PHP Build, Test și Deploy)

---

## 1. Scopul lucrării

Scopul lucrării este realizarea unui proces complet de CI/CD pentru o aplicație PHP utilizând:

- **Jenkins** pentru orchestrarea pipeline-urilor  
- **Docker & Docker Compose** pentru infrastructură multi-container  
- **Ansible** pentru configurarea automată a serverului și deploy  

Rezultatul final:  
Un pipeline complet care **build-uiește, testează și deploy-ază** aplicația PHP pe un server de test.

---

## 2. Arhitectura proiectului

Infrastructura este creată prin:

```
lab05/compose.yaml
```

Containerele pornite:

| Serviciu             | Rol                                | Porturi            |
|----------------------|-------------------------------------|---------------------|
| jenkins-controller   | Server Jenkins                      | 8080, 50000         |
| ssh-agent            | Agent Jenkins pentru build & test   | 2222                |
| ansible-agent        | Agent Jenkins pentru Ansible        | 2223                |
| test-server          | Server Apache pentru deploy         | 8081, 2224          |

---

## 3. Configurarea Jenkins Controller

1. Pornirea serverului:

```bash
docker compose up -d jenkins-controller
```

2. Acces Jenkins la:  
**http://localhost:8080**

3. Instalare plugin-uri:
- Git
- SSH Slaves / SSH Agent
- Pipeline
- Docker Pipeline

4. Crearea credențialelor SSH pentru:
- ssh-agent
- ansible-agent
- ansible → test-server

5. Crearea a două noduri noi:
- **ssh-agent** (pentru build & test)
- **ansible-agent** (pentru rularea Ansible)

---

## 4. Agentul SSH (Build & Test)

Fișiere implicate:

- `lab05/Dockerfile.ssh_agent`
- `lab05/keys/jenkins_to_ssh.pub`

Conține:

- Ubuntu 22.04
- openssh-server
- OpenJDK 17
- PHP CLI + extensii
- Git
- Composer
- PHPUnit

Probleme rezolvate:

- Lipsa `/run/sshd` → creat la build  
- Lipsa Java → instalat openjdk-17  
- Configurare chei SSH pentru Jenkins  

Acest agent rulează pipeline-ul de build și test.

---

## 5. Agentul Ansible

Fișiere:

- `lab05/Dockerfile.ansible_agent`
- `lab05/keys/ansible_to_test` (private)
- `lab05/keys/ansible_to_test.pub` (public)

Include:

- Ansible
- Python3
- SSH server
- OpenJDK 17

Conexiune testată cu:

```bash
ssh -i /home/jenkins/.ssh/ansible_to_test ansible@test-server -o StrictHostKeyChecking=no
```

---

## 6. Serverul de test (Apache + PHP)

Fișier:

- `lab05/Dockerfile.test_server`

Include:

- Apache2
- PHP + extensii
- SSH server
- User `ansible` autorizat prin chei

Porturi:

- **8081** – acces aplicație PHP  
- **2224** – SSH pentru deploy  

---

## 7. Ansible

Folder: `lab05/ansible/`

### 7.1 hosts.ini

```ini
[test_server]
test-server ansible_user=ansible ansible_ssh_private_key_file=/home/jenkins/.ssh/ansible_to_test ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

### 7.2 setup_test_server.yml

Acțiuni:

- instalare Apache + PHP
- creare `/var/www/php-app`
- configurare virtual host
- restart Apache

### 7.3 deploy_php.yml

Acțiuni:

- clonare repo
- copiere aplicație în `/var/www/php-app/`
- setare permisiuni `www-data`
- restart Apache

---

## 8. Pipeline-urile Jenkins

Sursa:  
```
lab05/pipelines/
```

### 8.1 Build & Test  
Fișier: `php_build_and_test_pipeline.groovy`  
Rulează pe **ssh-agent**

Etape:
1. Checkout cod
2. Instalare dependențe Composer
3. Rulare PHPUnit
4. JUnit report

---

### 8.2 Setup Test Server  
Fișier: `ansible_setup_pipeline.groovy`  
Rulează pe **ansible-agent**

Comandă:

```bash
ansible-playbook -i ansible/hosts.ini ansible/setup_test_server.yml
```

---

### 8.3 Deploy PHP  
Fișier: `php_deploy_pipeline.groovy`

Comandă:

```bash
ansible-playbook -i ansible/hosts.ini ansible/deploy_php.yml
```

---

## 9. Accesarea aplicației

După execuția pipeline-urilor:

1. php-build-and-test  
2. ansible-setup-test-server  
3. php-deploy-to-test-server  

Aplicația este accesibilă la:

👉 http://localhost:8081  
👉 http://localhost:8081/index.php  

---

## 10. Probleme întâlnite și soluții

### 1. Agenții Jenkins offline
**Cauză:** lipsa OpenJDK sau /run/sshd  
**Soluție:** instalare openjdk + mkdir /run/sshd + ssh-keygen -A

### 2. Composer nu se instala global
**Soluție:** instalare locală în workspace

### 3. Ansible: Host key verification failed
**Soluție:**  
`ansible_ssh_common_args='-o StrictHostKeyChecking=no'`

### 4. Apache dădea „Forbidden”
**Soluție:**  
`Require all granted` + permisiuni www-data

### 5. Jenkins nu găsea pipeline-ul
**Soluție:**  
Corectarea branch-ului (automation) și căii fișierului.

---

## 11. Concluzie

Laboratorul demonstrează integrarea completă CI/CD prin:

- Jenkins (automatizare)
- Docker (infrastructură locală)
- Ansible (configurare server și deploy)

Pipeline-ul final:

✔ build și test automat PHP  
✔ configurare completă server Apache  
✔ deploy automat pe server de test  

Este o implementare reală a unui flux DevOps profesional.

---
