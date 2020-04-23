pipeline {
    agent { docker { image 'python:3.8.2' } }
    stages {
        stage('build') {
            steps {
                sh 'python -m venv env'
                sh 'chmod +x env/bin/activate'
                sh '/env/bin/./activate'
                sh 'pip install -r requirements.txt'
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