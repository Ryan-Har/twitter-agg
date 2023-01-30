/* Requires the Docker Pipeline plugin */
pipeline {
    agent any
    environment {
        IMAGE = '677374482341.dkr.ecr.eu-west-2.amazonaws.com/twitter-agg'
    }
    stages {
        stage('build') {
            steps {
                withCredentials([string(credentialsId: 'ac58a311-104d-4d01-b816-64a16093ccb2', variable: 'BEARER')]) {
                sh "echo ${BEARER} > twitter.env"
                sh 'docker compose build'
                }
            }
        }
        stage('test') {
            steps{
                sh 'docker compose up -d'
                sleep(5)
                sh 'curl -L 127.0.0.1:5000'
            }
            post {
                always {
                    sh 'docker compose down'
                }
            }
        }
        stage('retag image'){
            steps{
                sh 'docker tag ${IMAGE}:latest ${IMAGE}:${BUILD_NUMBER}'
            }
        }
        stage('push image'){
            steps{
                script{
                    withDockerRegistry([url: 'https://${IMAGE}', credentialsId: 'ecr:eu-west-2:a9f0514f-824e-4e29-846f-de87a54374bb']) {
                        container = docker.image('677374482341.dkr.ecr.eu-west-2.amazonaws.com/twitter-agg')
                        container.push('latest')
                        container.push("${BUILD_NUMBER}")
                    }
                }
            }
        }    
    }
}
