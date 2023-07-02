pipeline {
    agent {label 'agent'}
	
    stages {
		stage('Build') {
            steps {
                echo 'Building....'
                sh 'sudo docker build -t ownedbyben/my_repo .'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
				sh 'yes | sudo docker system prune -a'
                sh 'sudo docker run --name weather -d -p 80:5000 ownedbyben/my_repo'
                sh 'sudo docker exec -d weather python3 unit-test.py'
            }
        }
		
		stage('UploadToDockerHub') {
			
			steps {
				echo 'Upload to dockerhub...'
                sh 'docker login -u ownedbyben -p dckr_pat_Xsj5Enay6Mzg9SuiXyE-c8Ai79M'
                sh 'docker tag ownedbyben/my_repo ownedbyben/my_repo:${BUILD_NUMBER}'
                sh 'docker push ownedbyben/my_repo:${BUILD_NUMBER}'
                sh 'docker tag ownedbyben/my_repo ownedbyben/my_repo:latest'
                sh 'docker push ownedbyben/my_repo:latest'
			}
        }

																																																						
        stage('Deploy') {
            environment {
                my_secret= credentials('duckerhub_token')
            }
            steps {
                echo 'Deploying....'
				sh """
					ssh -o StrictHostKeyChecking=no -i "/home/ec2-user/Key-instance1.pem" ec2-user@172.31.29.236 <<- _EOF_
					echo ${my_secret} | sudo docker login -username ownedbyben --password-stdin
					sudo docker pull ownedbyben/my_repo:latest
					sudo docker stop weather && sudo docker container rm weather
					sudo docker run --name weather -d -p 80:5000 ownedbyben/my_repo:latest
				_EOF_"""				
            }
        }

		stage('Clean'){
            steps {
                echo 'Cleaning...'
                sh 'sudo docker stop weather && sudo docker container rm weather'
                sh 'sudo docker image rm ownedbyben/my_repo:${BUILD_NUMBER}'
            }
        }
    }

	post {
			success {
				slackSend(channel: "#succeeded-build", message: "Build Success ${env.JOB_NAME} ${env.BUILD_NUMBER}")
			}

			failure {
                sh 'sudo docker stop weather && sudo docker container rm weather'
                sh 'sudo docker image rm ownedbyben/my_repo:${BUILD_NUMBER}'
				slackSend(channel: "#devops-alert", message: "Build failed ${env.JOB_NAME} ${env.BUILD_NUMBER}")
			}		
		}
}













