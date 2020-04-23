pipeline {
    agent { docker { image 'python:3.8.2' } }
    stages {
        stage('build') {
            steps {
                bash 'python -m venv env'
                bash 'source ./env/bin/activate'
                bash 'pip install -r requirements.txt'
                bash 'pip install pytest'
            }
        }
        stage('test') {
            steps {
                bash 'python -m pytest tests/'
            }
        }
    }
}