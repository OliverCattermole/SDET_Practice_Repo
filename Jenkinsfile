// Jenkinsfile
pipeline {
    agent any

    environment {
        // Shared config for tests. Sensitive info stays in withCredentials below.
        API_BASE_URL = 'https://jsonplaceholder.typicode.com'
    }

    stages {
        stage('Setup Environment') {
            steps {
                script {
                    echo "Updating package lists and installing Python dependencies..."
                    sh 'apt-get update'
                    sh 'apt-get install -y python3 python3-venv'

                    echo "Creating and activating virtual environment..."
                    // Setup venv and pull in dependencies
                    sh 'python3 -m venv venv_jenkins'
                    sh '. venv_jenkins/bin/activate'

                    echo "Installing Python project dependencies (including flake8)..."
                    sh 'venv_jenkins/bin/pip install -r requirements.txt'

                    echo "Installing Playwright browser binaries and dependencies..."
                    // Playwright needs both the binaries and system-level libs
                    sh 'venv_jenkins/bin/playwright install'
                    sh 'venv_jenkins/bin/playwright install-deps'
                }
            }
        }

        stage('Code Quality Check') {
            steps {
                script {
                    echo "Running Flake8 code quality checks..."
                    // Run flake8 on Test_Scripts directory
                    // --show-source: shows the line of code causing the warning
                    // --statistics: shows counts for each type of warning/error
                    // || true prevents linting errors from killing the whole build
                    //         Remove '|| true' if you want linting errors to FAIL the build.
                    sh 'venv_jenkins/bin/flake8 Test_Scripts/ --show-source --statistics || true'
                    echo "Flake8 check complete."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "Running Pytest tests..."
                    // Running in parallel (-n auto) to speed up execution
                    sh '''
                        export API_BASE_URL="${API_BASE_URL}"
                        venv_jenkins/bin/pytest -s -v -n auto --alluredir=allure-results Test_Scripts/test_web_example.py Test_Scripts/test_api_example.py
                    '''
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure([
                    reportBuildPolicy: 'ALWAYS', // Always generate report
                    results: [
                        [path: 'allure-results']
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
            sh 'rm -rf venv_jenkins' // Clean up virtual environment
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
