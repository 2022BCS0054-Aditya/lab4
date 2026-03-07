pipeline {
    agent any
    environment {
        DOCKER_USER = '2022bcs0054aditya'
        ROLL_NO = '2022BCS0054'
        IMAGE_NAME = "${DOCKER_USER}/wine_predict_2022bcs054_lab4"
    }
    stages {
        stage('Checkout') { // Stage 1
            steps {
                checkout scm
            }
        }
        stage('Setup Environment') { // Stage 2
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Train Model') { 
            steps {
                sh '''
                    . venv/bin/activate
                    python train.py
                '''
            }
        }
        stage('Read Accuracy') { // Stage 4 [cite: 109]
            steps {
                script {
                    // Extract r2_score (accuracy) from metrics.json 
                    def metrics = readJSON file: 'outputs/results.json'
                    env.NEW_ACCURACY = metrics.r2_score
                } 
            }
        }
        stage('Compare Accuracy') { // Stage 5
            steps {
                withCredentials([string(credentialsId: 'best-accuracy', variable: 'BEST_ACC')]) {
                    script {
                        // Compare current against baseline
                        def isBetter = (env.NEW_ACCURACY.toFloat() > BEST_ACC.toFloat())
                        env.BETTER = isBetter ? 'true' : 'false'
                        
                        if (env.BETTER == 'false') {
                            echo "${ROLL_NO}:----Metric did not improve"
                        }
                    }
                }
            }
        }
        stage('Build Docker Image') { // Stage 6
            when { environment name: 'BETTER', value: 'true' } // Conditional
            steps {
                script {
                    // Build using Docker Hub credentials
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest ."
                }
            }
        }
        stage('Push Docker Image') { // Stage 7
            when { environment name: 'BETTER', value: 'true' } // Conditional 
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                    sh "docker push ${IMAGE_NAME}:latest" 
                }
            }
        }
    }
    post {
        always {
            // Task 5: Archive artifacts regardless of success/failure [cite: 122, 123]
            archiveArtifacts artifacts: 'outputs/**', fingerprint: true // [cite: 124, 125]
        }
    }
}