node {
    checkout scm
    def myTestContainer = docker.image('python:3.8.2')
    myTestContainer.pull()
    properties(
        [
            pipelineTriggers([pollSCM('* * * * *')])
        ]
    )
    stage('Preparation') {
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
    stage('Unit Tests') {
        myTestContainer.inside {
            sh '''#!/bin/bash
                source env/bin/activate
                python -m pytest tests/unit/
            '''
        }
    }
    stage('Integration Tests') {
        myTestContainer.inside {
            sh '''#!/bin/bash
                source env/bin/activate
                python -m pytest tests/integration/
            '''
        }
    }
    stage('System Tests') {
        myTestContainer.inside {
            sh '''#!/bin/bash
                source env/bin/activate
                python -m pytest tests/system/
            '''
        }
    }
}