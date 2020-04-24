node {
    docker.image('python:3.8.2').inside {
        stage('Checkout') {
            checkout scm
        }
        state('Install Deps') {
            sh '''#!/bin/bash
                python -m venv env
                source env/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt --no-cache-dir
                pip install pytest --no-cache-dir
            '''
        }
        stage('unit tests') {
            sh '''#!/bin/bash
                python -m pytest tests/unit/
            '''
        }
        stage('integration tests') {
            sh '''#!/bin/bash
                python -m pytest tests/integration/
            '''
        }
        stage('system tests') {
            sh '''#!/bin/bash
                python -m pytest tests/system/
            '''
        }
    }
}