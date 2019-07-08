def gitSHA

podTemplate(
    label: 'mypod', 
    inheritFrom: 'default',
    containers: [
        containerTemplate(
            name: 'python', 
            image: 'python:3-alpine',
            ttyEnabled: true,
            command: 'cat'
        ),
        containerTemplate(
            name: 'docker', 
            image: 'docker:18.02',
            ttyEnabled: true,
            command: 'cat'
        ),
        containerTemplate(
            name: 'kubectl', 
            image: 'gcr.io/cloud-builders/kubectl',
            ttyEnabled: true,
            command: 'cat'
        )
    ],
    volumes: [
        hostPathVolume(
            hostPath: '/var/run/docker.sock',
            mountPath: '/var/run/docker.sock'
        )
    ]
) {
  node("mypod") {
    // replace  "your_repo"  to your docker repo name 
     environment {
     registry = "docker.io/azimuth3d/flaskapp"
     registryCredential = ‘dockerhub’
    }
    stage('Checkout') {
      steps {
        checkout scm
        script {
          gitSHA = sh(returnStdout: true, script: 'git rev-parse --short HEAD')
        }
      }
    }
    stage('Install') {
        container('python') {
          sh 'pip install -r requirements.txt'
        }
    }
    stage('Test') {
        container('python') {
          sh 'pytest'
        }
    }
    stage('Build') {
      environment {
        TAG = "$gitSHA"
      }
        container('docker') {
          docker.build registry + ":$TAG"
          docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
    }
    stage('Deploy Canary') {
      when { branch 'canary' }
        container('kubectl') {
          sh "export TAG=$gitSHA" + 'envsubst < deployment/canary.yaml | kubectl apply -f -'
          sh "export PROD_WEIGHT=95 CANARY_WEIGHT=5" + 'envsubst < deployment/istio.yaml | kubectl apply -f -'
        }
    }
    stage('Deploy Production') {
      when { branch 'master' }
     
        container('kubectl') {
          sh "export TAG=$gitSHA" + 'envsubst < deployment/prod.yaml | kubectl apply -f -'
          sh "export PROD_WEIGHT=100 CANARY_WEIGHT=0" + 'envsubst < deployment/istio.yaml | kubectl apply -f -'
        }
    }
  }
}
  
