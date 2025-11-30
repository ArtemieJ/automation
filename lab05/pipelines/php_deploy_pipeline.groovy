pipeline {
    agent { label 'ansible-agent' }

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout repo') {
            steps {
                git branch: 'automation',
                    url: 'https://github.com/ArtemieJ/automation.git'
            }
        }

        stage('Deploy PHP app via Ansible') {
            steps {
                dir('lab05') {
                    sh '''
                        ansible-playbook -i ansible/hosts.ini ansible/deploy_php.yml
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'PHP app has been deployed to test server.'
        }
        failure {
            echo 'PHP deploy failed.'
        }
    }
}
