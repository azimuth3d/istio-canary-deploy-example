def gitSHA
def image = "docker.io/azimuth3d/flaskapp:${env.BUILD_ID}"

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
            image: 'amaceog/kubectl',
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

    stage('Checkout') {
        checkout scm
        script {
          gitSHA = sh(returnStdout: true, script: 'git rev-parse --short HEAD')
        }
    }
    stage('Install') {
        container('python') {
          sh 'pip install -r requirements.txt'
        }
    }
  /*    stage('Test') {
        container('python') {
          sh 'pytest'
        }
    }
    */
    stage('Build') {
       container('docker') {
        sh "docker build --no-cache -t flaskapp:latest ."
      }
    }

    stage('Push Image') {
       withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'DOCKER_PASSWD', usernameVariable: 'DOCKER_USER')]) {
          container('docker') {
            sh '''
            echo ${DOCKER_PASSWD} | docker login -u ${DOCKER_USER} --password-stdin
              '''
            sh "docker tag flaskapp:latest  ${image}"
            sh "docker push ${image} && docker rmi ${image}"    
          }
        }
    }

    stage('Deploy') {
          switch(env.BRANCH_NAME) {
            case 'master':
                container('kubectl') {
                     sh 'apk update && apk add gettext'
                     sh "export TAG=$gitSHA"
                     sh 'envsubst < deployment/prod.yaml | kubectl apply -f -'
                     sh "export PROD_WEIGHT=100 CANARY_WEIGHT=0"
                     sh 'envsubst < deployment/istio.yaml | kubectl apply -f -'
                }
            case 'canary':
                  container('kubectl') {
                       sh 'apk update && apk add gettext'
                       sh "export TAG=$gitSHA" + 'envsubst < deployment/canary.yaml | kubectl apply -f -'
                       sh "export PROD_WEIGHT=80 CANARY_WEIGHT=20" + 'envsubst < deployment/istio.yaml | kubectl apply -f -'
                  }    
          }
         
        }
  }
}
  
