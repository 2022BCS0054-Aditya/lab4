pipeline {
    agent any
    environment {
        DOCKER_USER = '2022bcs0054aditya' 
        IMAGE_NAME = "${DOCKER_USER}/wine_predict_2022bcs054_lab4:latest"
        CONTAINER_NAME = "inference-validator-2022bcs0054"
    }
    stages {
        stage('Pull Image') { // Stage 1
            steps {
                sh "docker pull ${IMAGE_NAME}"
            }
        }
        stage('Run Container') { // Stage 2
            steps {
                // Mapping to 8001 as required
                sh "docker run -d -p 8001:8001 --name ${CONTAINER_NAME} ${IMAGE_NAME}"
            }
        }
        stage('Wait for Service') { // Stage 3
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    sh '''
                        until curl -s http://localhost:8001/predict > /dev/null; do 
                            echo "Waiting for API..."
                            sleep 3
                        done
                    ''' 
                }
            }
        }
        stage('Send Valid Inference Request') { // Stage 4 
            steps {
                sh '''
                    echo "Testing Valid Input..."
                    RESPONSE=$(curl -s -X POST http://localhost:8001/predict \
                        -H "Content-Type: application/json" \
                        -d @test_inputs/valid_input.json) 
                    
                    echo "Response: $RESPONSE" // 
                    
                    # Validation logic
                    echo $RESPONSE | jq -e '.wine_quality' | grep -E '^[0-9]+$'
                '''
            }
        }
        stage('Send Invalid Request') { // Stage 5
            steps {
                sh '''
                    echo "Testing Invalid Input..."
                    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8001/predict \
                        -H "Content-Type: application/json" \
                        -d @test_inputs/invalid_input.json)
                    
                    echo "HTTP Status Received: $HTTP_STATUS" // 
                    
                    if [ "$HTTP_STATUS" -ge 400 ]; then
                        echo "Success: API correctly rejected invalid input."
                    else
                        echo "Failure: API accepted invalid input with status $HTTP_STATUS"
                        exit 1
                    fi
                '''
            }
        }
    }
    post {
        always {
            // Stage 6: Stop and remove container 
            sh "docker stop ${CONTAINER_NAME} || true && docker rm ${CONTAINER_NAME} || true"
        }
        success {
            echo "Pipeline Result: PASS"
        }
        failure {
            echo "Pipeline Result: FAIL"
        }
    }
}