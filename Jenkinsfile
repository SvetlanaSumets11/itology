pipeline {
  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    ansiColor('xterm')
    timestamps()
    timeout(time: 20, unit: 'MINUTES')
  }
  agent {
    dockerfile { filename 'Dockerfile.build' }
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Setup') {
      steps {
        script {
          sh """
          python -m pip install --upgrade pip &&
          python -m pip install poetry &&
          python -m poetry config virtualenvs.create false &&
          python -m poetry install
          """
        }
      }
    }
    stage('Linting') {
      steps {
        script {
          sh """
          flake8 .
          """
        }
      }
    }
    stage('Unit Testing') {
      steps {
        script {
          sh """
          pytest .
          """
        }
      }
    }
  }
  post {
    failure {
      script {
        msg = "Build error for ${env.JOB_NAME} ${env.BUILD_NUMBER} (${env.BUILD_URL})"
    }
  }
}
