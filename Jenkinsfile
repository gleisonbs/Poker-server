node {
    def myTestContainer = docker.image('python:3.8.2')
    myTestContainer.pull()
    stage('Preparation') {
        checkout scm
        myTestContainer.inside {
            sh '''#!/bin/bash
                python -m venv env
                source env/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt --no-cache-dir
                pip install pytest --no-cache-dir
            '''
        }
    }
    stage('Test') {
        myTestContainer.inside {
            sh '''#!/bin/bash
                source env/bin/activate
                python -m pytest tests/
            '''
        }
    }
}