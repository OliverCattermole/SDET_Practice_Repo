// Jenkinsfile (Updated with jenkins/jnlp-agent-docker image)
pipeline {
    agent {
        docker {
            // Use the agent image that comes with the Docker CLI pre-installed
            image 'jenkins/jnlp-agent-docker'
            // Only mount the Docker socket from the host.
            // The 'docker' binary is already inside the 'jenkins/jnlp-agent-docker' image.
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    // Your environment variables are good.
    environment {
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_NAME = 'test_database'
    }

    stages {
        stage('Prepare Agent Environment') {
            steps {
                script {
                    echo "Updating package lists and installing Python dependencies..."
                    // 'jenkins/jnlp-agent-docker' is based on Debian/Ubuntu, so apt-get works.
                    // It already has curl, gnupg, etc., and the Docker CLI.
                    // We only need to install Python-related tools and libpq-dev for psycopg2.
                    sh 'apt-get update'
                    sh 'apt-get install -y python3 python3-venv libpq-dev'

                    echo "Creating and activating virtual environment..."
                    sh 'python3 -m venv venv_jenkins'
                    sh '. venv_jenkins/bin/activate'

                    echo "Installing Python project dependencies including psycopg2-binary..."
                    sh 'venv_jenkins/bin/pip install -r requirements.txt psycopg2-binary'

                    echo "Installing Playwright browser binaries and dependencies..."
                    // These are still needed unless you switch to Playwright's own Docker browser images.
                    sh 'venv_jenkins/bin/playwright install'
                    sh 'venv_jenkins/bin/playwright install-deps'
                }
            }
        }

        // ... Rest of your stages (Setup Containerized Test Environment, Run Automated Tests, etc.)
        //    remain the same as they use 'docker compose' which will now be found.

        stage('Setup Containerized Test Environment') {
            steps {
                script {
                    echo "Starting Docker Compose services in detached mode..."
                    sh 'docker compose up -d --build' // This should now work!

                    echo "Waiting for test_db service to be ready..."
                    withCredentials([usernamePassword(credentialsId: 'MY_DUMMY_USER_PASS', usernameVariable: 'DB_USER_VAR', passwordVariable: 'DB_PASS_VAR')]) {
                        sh '''
                            venv_jenkins/bin/python -c "
import psycopg2
import time
import os

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER_VAR')
DB_PASS = os.getenv('DB_PASS_VAR')

print(f'Attempting to connect to DB at {DB_HOST}:{DB_PORT}/{DB_NAME} with user {DB_USER}')

for i in range(20):
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname=DB_NAME)
        conn.close()
        print('Database is ready!')
        break
    except psycopg2.OperationalError as e:
        print(f'Database not ready yet (Attempt {i+1}/20): {e}. Waiting 5 seconds...')
        time.sleep(5)
else:
    raise Exception('Database did not become ready in time after multiple attempts!')
"
                        '''
                    }
                }
            }
        }

        stage('Run Automated Tests') {
            steps {
                script {
                    echo "Running Pytest tests against the containerized services..."
                    withCredentials([usernamePassword(credentialsId: 'MY_DUMMY_USER_PASS', usernameVariable: 'DB_USER_FOR_TESTS', passwordVariable: 'DB_PASS_FOR_TESTS')]) {
                        sh '''
                            export DB_HOST=${DB_HOST}
                            export DB_PORT=${DB_PORT}
                            export DB_NAME=${DB_NAME}
                            export DB_USER=${DB_USER_FOR_TESTS}
                            export DB_PASS=${DB_PASS_FOR_TESTS}

                            venv_jenkins/bin/pytest -s -v -n auto --alluredir=allure-results Test_Scripts/test_web_example.py Test_Scripts/test_api_example.py
                        '''
                    }
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure([
                    reportBuildPolicy: 'ALWAYS',
                    results: [
                        [path: 'allure-results']
                    ]
                ])
            }
        }

        stage('Use Secret Credentials') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'MY_DUMMY_API_TOKEN', variable: 'API_TOKEN_VAR')]) {
                        sh '''
                        echo "Attempting to use API Token..."
                        echo "API_Token_Start: ${API_TOKEN_VAR}"
                        echo "curl -H \\"Authorization: Bearer ${API_TOKEN_VAR}\\" https://api.example.com/data"
                        echo "API_Token_End: ${API_TOKEN_VAR}"
                        '''
                    }

                    withCredentials([usernamePassword(credentialsId: 'MY_DUMMY_USER_PASS', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASS')]) {
                        sh '''
                        echo "Attempting to connect to Database..."
                        echo "DB_User_Start: ${DB_USER}"
                        echo "DB_Pass_Start: ${DB_PASS}"
                        echo "mysql -u ${DB_USER} -p${DB_PASS} database_name"
                        echo "DB_User_End: ${DB_USER}"
                        echo "DB_Pass_End: ${DB_PASS}"
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            steps {
                echo "Tearing down Docker Compose services..."
                sh 'docker compose down'

                echo "Cleaning up virtual environment..."
                sh 'rm -rf venv_jenkins'
            }
        }
        failure {
            echo 'Pipeline failed! Check console output for details.'
        }
        success {
            echo 'Pipeline succeeded!'
        }
    }
}