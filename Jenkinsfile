pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
    }

    environment {
        FUNCTION_NAME      = 'my-api-function'
        ALIAS              = 'prod'
        AWS_DEFAULT_REGION = 'ap-southeast-2'
        AWS_PAGER          = ''
        API_URL            = 'https://e55r5pw1y6.execute-api.ap-southeast-2.amazonaws.com/'
    }

    stages {
        stage('Test') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --quiet pytest
                pytest tests/
                '''
            }
        }

        stage('Package') {
            steps {
                sh '''
                . venv/bin/activate
                rm -rf package function.zip
                mkdir package
                if grep -qvE '^\\s*(#|$)' requirements.txt; then
                    pip install -r requirements.txt -t package/
                fi
                cp app/*.py package/
                cd package && zip -r ../function.zip .
                '''
            }
        }

        stage('Deploy') {
            steps {
                script {
                    env.PREV_VERSION = sh(
                        script: 'aws lambda get-alias --function-name $FUNCTION_NAME --name $ALIAS --query FunctionVersion --output text',
                        returnStdout: true).trim()

                    sh 'aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://function.zip'
                    sh 'aws lambda wait function-updated --function-name $FUNCTION_NAME'

                    env.NEW_VERSION = sh(
                        script: 'aws lambda publish-version --function-name $FUNCTION_NAME --query Version --output text',
                        returnStdout: true).trim()

                    sh 'aws lambda update-alias --function-name $FUNCTION_NAME --name $ALIAS --function-version $NEW_VERSION'
                    echo "Deployed version ${env.NEW_VERSION} (previous: ${env.PREV_VERSION})"
                }
            }
        }

        stage('Smoke Test') {
            steps {
                sh 'sleep 5 && curl -fsS $API_URL'
            }
        }
    }

    post {
        failure {
            script {
                if (env.NEW_VERSION && env.PREV_VERSION) {
                    echo "Rolling back alias ${env.ALIAS} to version ${env.PREV_VERSION}"
                    sh 'aws lambda update-alias --function-name $FUNCTION_NAME --name $ALIAS --function-version $PREV_VERSION'
                }
            }
        }
        success {
            echo 'Deployment successful!'
        }
        cleanup {
            sh 'rm -rf package function.zip'
        }
    }
}
