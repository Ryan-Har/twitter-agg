/* Requires the Docker Pipeline plugin */
pipeline {
    agent none
    stages {
        stage('build') {
            steps {
                withCredentials([file(credentialsId: '0608dc10-a11e-44dd-925c-63f4b58dba46', variable: 'BEARER')]) {
                sh('#!/bin/sh -e\n' + 'echo $BEARER > twitter.env')
                sh 'docker compose build'
                }
            }
        }
        stage('test') {
            steps{
                sh 'curl 127.0.0.1:5000'
            }
        }
    }
}
