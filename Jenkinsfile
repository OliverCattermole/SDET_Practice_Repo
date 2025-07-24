// Jenkinsfile
pipeline {
    agent any // Tells Jenkins to run this pipeline on any available agent (your Docker container in this case)

    // It's good practice to define environment variables for consistency
    // However, sensitive data should still use withCredentials as you correctly do.
    environment {
        // Define common variables needed by your tests to connect to the DB
        DB_HOST = 'localhost' // If tests run on Jenkins agent and connect via mapped port
        DB_PORT = '5432'
        DB_NAME = 'test_database' // From your docker-compose.yml
    }

    stages {
        stage('Prepare Agent Environment') {
            steps {
                script { // 'script' block allows execution of shell commands
                    // Update package lists and install python3 and venv module
                    echo "Updating package lists and installing Python dependencies..."
                    sh 'apt-get update'
                    sh 'apt-get install -y python3 python3-venv'

                    // Create and activate a virtual environment
                    echo "Creating and activating virtual environment..."
                    sh 'python3 -m venv venv_jenkins'
                    sh '. venv_jenkins/bin/activate' // Using '.' for POSIX compatibility

                    // Install Python dependencies (including requests and allure-pytest)
                    echo "Installing Python project dependencies"
                    sh 'venv_jenkins/bin/pip install -r requirements.txt' // psycopg2-binary is easier to install

                    // Install Playwright browser binaries and dependencies
                    echo "Installing Playwright browser binaries and dependencies..."
                    sh 'venv_jenkins/bin/playwright install'
                    sh 'venv_jenkins/bin/playwright install-deps' // Ensure system dependencies are also installed

                    // Run your Pytest tests and generate Allure results
                    // The '.' means "discover tests in the current directory (Test_Scripts)"
                    // sh 'venv_jenkins/bin/pytest -s -v -n auto --alluredir=allure-results Test_Scripts/test_web_example.py Test_Scripts/test_api_example.py'
                }
            }
        }

        stage('Setup Containerized Test Environment') {
            steps {
                script {
                    echo "Starting Docker Compose services in detached mode..."
                    // Ensure docker-compose.yml is in the workspace root
                    // --build will rebuild images if changes detected (useful for 'my_api' if you add one)
                    sh 'docker compose up -d --build'

                    // --- CRUCIAL: Waiting for Database to be Ready ---
                    echo "Waiting for test_db service to be ready..."
                    // We'll use your existing MY_DUMMY_USER_PASS credential for this check
                    withCredentials([usernamePassword(credentialsId: 'MY_DUMMY_USER_PASS', usernameVariable: 'DB_USER_VAR', passwordVariable: 'DB_PASS_VAR')]) {
                        sh '''
                            # Run Python script inside the virtual environment
                            venv_jenkins/bin/python -c "
import psycopg2
import time
import os

DB_HOST = os.getenv('DB_HOST') # Get from Jenkins environment block
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER_VAR') # From Jenkins credentials
DB_PASS = os.getenv('DB_PASS_VAR') # From Jenkins credentials

print(f'Attempting to connect to DB at {DB_HOST}:{DB_PORT}/{DB_NAME} with user {DB_USER}')

for i in range(20): # Increased attempts for more robustness on CI
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

        stage('Run Automated Tests') { // Renamed for clarity
            steps {
                script {
                    echo "Running Pytest tests against the containerized services..."
                    // Your tests now connect to the services exposed by Docker Compose
                    // Ensure your Python API tests use the DB_HOST, DB_PORT, DB_NAME
                    // and your credentials (DB_USER_VAR, DB_PASS_VAR) to connect to the DB.
                    withCredentials([usernamePassword(credentialsId: 'MY_DUMMY_USER_PASS', usernameVariable: 'DB_USER_FOR_TESTS', passwordVariable: 'DB_PASS_FOR_TESTS')]) {
                        // Pass DB credentials to your test run as environment variables.
                        // Your Python tests can then pick these up using os.getenv().
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
                // The allure plugin provides this step directly.
                // The path is relative to the Jenkins workspace root.
                // If 'cd Test_Scripts' was used above, the results will be in Test_Scripts/allure-results.
                allure([
                    reportBuildPolicy: 'ALWAYS', // Always generate report
                    results: [
                        [path: 'allure-results'] // Path to allure-results folder
                    ]
                ])
            }
        }

        stage('Use Secret Credentials') {
            steps {
                script {
                    // --- Using Secret Text Credential ---
                    // 'string' type for Secret Text
                    withCredentials([string(credentialsId: 'MY_DUMMY_API_TOKEN', variable: 'API_TOKEN_VAR')]) {
                        sh '''
                        echo "Attempting to use API Token..."
                        # NEVER print the raw variable directly in production: echo "API_TOKEN_VAR: $API_TOKEN_VAR"
                        # Simulate usage, Jenkins will mask it if the value is detected:
                        echo "API_Token_Start: ${API_TOKEN_VAR}" # This will be masked in logs
                        echo "curl -H \\"Authorization: Bearer ${API_TOKEN_VAR}\\" https://api.example.com/data"
                        echo "API_Token_End: ${API_TOKEN_VAR}"
                        '''
                    }

                    // --- Using Username with Password Credential ---
                    // 'usernamePassword' type for Username with Password
                    withCredentials([usernamePassword(credentialsId: 'MY_DUMMY_USER_PASS', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASS')]) {
                        sh '''
                        echo "Attempting to connect to Database..."
                        # Access username as $DB_USER and password as $DB_PASS
                        echo "DB_User_Start: ${DB_USER}" # This will be masked in logs
                        echo "DB_Pass_Start: ${DB_PASS}" # This will be masked in logs
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
            // All actions (steps) go directly into the 'always' block
            // or wrapped in a 'script { ... }' block if they are Groovy commands.
            steps { // You need a 'steps' block directly inside 'always'
                echo "Tearing down Docker Compose services..."
                sh 'docker compose down' // Stop and remove containers, networks

                echo "Cleaning up virtual environment..."
                sh 'rm -rf venv_jenkins' // Still clean up virtual environment
            }
        }
        failure {
            // Steps to run only if the pipeline fails
            echo 'Pipeline failed! Check console output for details.'
        }
        success {
            // Steps to run only if the pipeline succeeds
            echo 'Pipeline succeeded!'
        }
    }
}