pipeline {
    agent { label 'ansible-agent' }

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout repo with Ansible playbook') {
            steps {
                git branch: 'automation',
                    url: 'https://github.com/ArtemieJ/automation.git'
            }
        }

        stage('Run Ansible playbook (setup_test_server)') {
            steps {
                dir('lab05') {
                    sh '''
                        ansible-playbook -i ansible/hosts.ini ansible/setup_test_server.yml
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Test server was configured successfully via Ansible.'
        }
        failure {
            echo 'Ansible setup failed.'
        }
    }
}
