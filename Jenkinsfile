// Jenkinsfile (Adapted for Docker-from-Docker on the Jenkins Agent)
pipeline {
    agent {
        docker {
            // Use an image that has the Docker CLI installed.
            // 'jenkins/jnlp-agent-docker' is a good choice if available,
            // or even a simple 'ubuntu:latest' and then mount the docker binary/socket.
            // A common pattern is to use an image that already includes many build tools,
            // or to build your own custom agent image.
            // For simplicity, let's use a standard Linux image and manually prepare it
            // by mounting what's needed.
            // A more direct option if you are using Docker Engine as agent's host:
            image 'ubuntu:latest' // Or 'python:3.10-slim-bookworm' if you prefer Python already there
            args '-v /var/run/docker.sock:/var/run/docker.sock -v /usr/bin/docker:/usr/bin/docker'
            // The above args are critical: they map the host's docker socket and binary into the agent container.
            // This means the 'docker' command inside the agent talks to the host's Docker daemon.
            // For a more robust setup, you might use 'jenkins/jnlp-agent-docker' or build your own.
        }
    }

    // Your environment variables are good.
    environment {
        DB_HOST = 'localhost' // If tests run on Jenkins agent and connect via mapped port
        DB_PORT = '5432'
        DB_NAME = 'test_database'
    }

    stages {
        stage('Prepare Agent Environment') {
            steps {
                script {
                    echo "Ensuring Python and venv are installed..."
                    // On a clean 'ubuntu:latest' image, you still need to install these.
                    // No 'sudo' needed here, as we are running as root inside this temporary container.
                    sh 'apt-get update && apt-get install -y python3 python3-venv libpq-dev curl gnupg'

                    echo "Creating and activating virtual environment..."
                    sh 'python3 -m venv venv_jenkins'
                    sh '. venv_jenkins/bin/activate'

                    echo "Installing Python project dependencies including psycopg2-binary..."
                    sh 'venv_jenkins/bin/pip install -r requirements.txt psycopg2-binary'

                    echo "Installing Playwright browser binaries and dependencies..."
                    // Note: If you use Playwright's own Docker images, these steps are often unnecessary.
                    sh 'venv_jenkins/bin/playwright install'
                    sh 'venv_jenkins/bin/playwright install-deps'
                }
            }
        }

        stage('Setup Containerized Test Environment') {
            steps {
                script {
                    echo "Starting Docker Compose services in detached mode..."
                    // 'docker' command should now be available because of the socket/binary mount
                    sh 'docker compose up -d --build'

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