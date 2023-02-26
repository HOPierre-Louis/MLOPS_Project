pipeline {
    agent any
    // Text from jenkins dev
    triggers {
        // Listen for Github webhooks
        githubPush()
    }
    
    environment{
        DOCKERHUB_CREDENTIALS = credentials('itsvincenzoh-dockerhub')
    }
  
    stages { 
        stage('Checkout') {
            steps {
                sshagent(credentials: ['github_shh']) {
                    sh "git checkout dev"
                    sh "git pull"
                    //sh "git branch -d staging"
                    sh "git checkout -b staging"
                    sh "git push --set-upstream origin staging"
                    sh "python3 --version"
                }
            }
        }
        stage('Building') {
            steps {
                // Install dependencies
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Testing') {
            steps {
                sh 'python3 -m unittest'
            }
        }
        stage('Deploying') {
            parallel {
                stage('Docker Image'){
                    steps {
                        // Build the Docker image
                        sh 'docker build -t itsvincenzoh/github-jenkins:latest .'

                        // Run a docker container from the image
                        sh 'docker run -d -p 6003:5000 itsvincenzoh/github-jenkins:latest'

                        // Login to Dockerhub
                        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'

                        // Push the image to Dockerhub
                        sh 'docker push itsvincenzoh/github-jenkins:latest'
                    }
                }
                stage('Merge branch'){
                    steps {
                        sshagent(credentials: ['github_shh']) {
                            sh '''
                                git checkout main
                                git merge staging
                                git branch -d staging
                                git push --set-upstream origin main
                                git push origin --delete staging
                            '''
                            
                        }
                    }
                }
            }

        }
        
    }
}
