pipeline {
    agent { docker { image 'python:3.8.2' } }
    stages {
        stage('build') {
            steps {
                sh 'pip install -r requirements'
                sh 'pip install pytest'
            }
        }
        stage('test') {
            steps {
                sh 'python -m pytest tests/'
            }
        }
    }
}