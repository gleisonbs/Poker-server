node {
    stage('Preparation') {
        checkout scm
    }
    stage('Test') {
        def myTestContainer = docker.image('python:3.8.2')
        myTestContainer.pull()
        myTestContainer.inside {
            sh 'pip install --upgrade pip'
            sh 'pip install -r requirements.txt --no-cache-dir --user'
            sh 'pip install pytest --no-cache-dir --user'
            sh 'python -m pytest tests/'
        }
    }
}