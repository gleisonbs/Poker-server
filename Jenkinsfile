pipeline {
    agent { docker { image 'python:3.8.2' } }
    stages {
        stage('build') {
            steps {
                sh 'pip install -r requirements.txt --user'
                sh 'pip install pytest --user'
            }
        }
        stage('test') {
            steps {
                sh 'python -m pytest tests/'
            }
        }
    }
}