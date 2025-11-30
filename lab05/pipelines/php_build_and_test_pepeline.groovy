pipeline {
    agent { label 'ssh-agent' }

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout PHP project') {
            steps {
                git branch: 'automation',
                    url: 'https://github.com/ArtemieJ/automation.git'
            }
        }

        stage('Install dependencies with Composer') {
            steps {
                dir('lab05/php-app') {
                    sh '''
                        if ! command -v composer >/dev/null 2>&1; then
                          echo "Composer not found, installing locally..."
                          php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
                          php composer-setup.php --install-dir=/usr/local/bin --filename=composer
                          rm composer-setup.php
                        fi

                        composer install
                    '''
                }
            }
        }

        stage('Run PHPUnit tests') {
            steps {
                dir('lab05') {
                    sh '''
                        php php-app/vendor/bin/phpunit tests
                    '''
                }
            }
        }
    }

    post {
        always {
            // dacă ai rapoarte JUnit din PHPUnit, poți adapta pattern-ul
            junit allowEmptyResults: true, testResults: 'lab05/tests/**/junit-*.xml'
        }
        failure {
            echo 'PHP build or tests failed.'
        }
        success {
            echo 'PHP build and tests completed successfully.'
        }
    }
}
