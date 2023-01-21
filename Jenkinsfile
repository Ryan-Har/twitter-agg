/* Requires the Docker Pipeline plugin */
pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                withCredentials([string(credentialsId: 'ac58a311-104d-4d01-b816-64a16093ccb2', variable: 'BEARER')]) {
                sh 'echo $BEARER > twitter.env'
                sh 'docker compose build'
                }
            }
        }
        stage('test') {
            steps{
                sh 'docker compose up'
                sh 'curl 127.0.0.1:5000'
            }
        }
    }
}
