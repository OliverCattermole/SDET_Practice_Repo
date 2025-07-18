// Jenkinsfile
pipeline {
    agent any // Tells Jenkins to run this pipeline on any available agent (your Docker container in this case)

    //environment {
        // Define environment variables if needed.
        // Example: PLAYWRIGHT_BROWSERS_PATH = '/ms-playwright'
    //}

    stages {
        stage('Setup Environment and Run Tests') {
            steps {
                script { // 'script' block allows execution of shell commands
                    // Update package lists and install python3 and venv module
                    sh 'apt-get update'
                    sh 'apt-get install -y python3 python3-venv'

                    // Create and activate a virtual environment
                    sh 'python3 -m venv venv_jenkins'
                    sh '. venv_jenkins/bin/activate' // Using '.' for POSIX compatibility

                    // Install Python dependencies (including requests and allure-pytest)
                    sh 'venv_jenkins/bin/pip install -r requirements.txt'

                    // Install Playwright browser binaries and dependencies
                    sh 'venv_jenkins/bin/playwright install-deps' // Ensure system dependencies are also installed

                    // Run your Pytest tests and generate Allure results
                    // The '.' means "discover tests in the current directory (Test_Scripts)"
                    sh 'venv_jenkins/bin/pytest -s -v -n auto --alluredir=allure-results Test_Scripts/test_web_example.py Test_Scripts/test_api_example.py'
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
            // You can add steps here that always run after all stages
            // For example, clean up workspace or send notifications
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