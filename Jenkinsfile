node {
    stage('Preparation') {
        checkout scm
    }
    stage('Test') {
        def myTestContainer = docker.image('python:3.8.2')
        myTestContainer.pull()
        myTestContainer.inside {
            sh '''#!/bin/bash
                python -m venv env
                source env/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt --no-cache-dir
                pip install pytest --no-cache-dir
                python -m pytest tests/
            '''
        }
    }
}