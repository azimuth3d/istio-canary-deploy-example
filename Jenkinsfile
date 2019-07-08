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
)
  // replace  "your_repo"  to your docker repo name 
  environment {
    registry = "docker.io/azimuth3d/flaskapp"
    registryCredential = ‘dockerhub’
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        script {
          gitSHA = sh(returnStdout: true, script: 'git rev-parse --short HEAD')
        }
      }
    }
    stage('Install') {
      steps {
        container('python') {
          sh 'pip install -r requirements.txt'
        }
      }
    }
    stage('Test') {
      steps {
        container('python') {
          sh 'pytest'
        }
      }
    }
    stage('Build') {
      environment {
        TAG = "$gitSHA"
      }
      steps {
        container('docker') {
      /*    sh 'docker login -u token -p ${REGISTRY_TOKEN} docker.io'
          sh 'docker build -t $IMAGE_REGISTRY/flaskapp:$TAG .'
          sh 'docker push $IMAGE_REGISTRY/flaskapp:$TAG' */
          docker.build registry + ":$TAG"
          docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
      }
    }
    stage('Deploy Canary') {
      when { branch 'canary' }
      steps {
        container('kubectl') {
          sh "export TAG=$gitSHA" + 'envsubst < deployment/canary.yaml | kubectl apply -f -'
          sh "export PROD_WEIGHT=95 CANARY_WEIGHT=5" + 'envsubst < deployment/istio.yaml | kubectl apply -f -'
        }
      }
    }
    stage('Deploy Production') {
      when { branch 'master' }
      steps {
        container('kubectl') {
          sh "export TAG=$gitSHA" + 'envsubst < deployment/app.yaml | kubectl apply -f -'
          sh "export PROD_WEIGHT=100 CANARY_WEIGHT=0" + 'envsubst < deployment/istio.yaml | kubectl apply -f -'
        }
      }
    }
  }
}