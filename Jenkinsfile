node {
    stage('Preparation') {
        checkout scm
    }
    stage('Test') {
        def myTestContainer = docker.image('python:3.8.2')
        myTestContainer.pull()
        myTestContainer.inside {
            sh 'pip install -r requirements.txt --user'
            sh 'pip install pytest --user'
            sh 'python -m pytest tests/'
        }
    }
}