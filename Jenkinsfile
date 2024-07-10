pipeline {
    agent any

    environment {
        DEPLOY_USER = 'vagrant'
        DEPLOY_HOST = '192.168.33.10'
        SSH_KEY = credentials('fastapi_Vagrant')
        GITHUB_TOKEN = credentials('github_token')
        PLINK_PATH = 'C:\\Program Files\\PuTTY\\plink.exe'
        PSCP_PATH = 'C:\\Program Files\\PuTTY\\pscp.exe'
        DEPLOY_PASSWORD = 'vagrant'
        REPO_URL = 'https://github.com/ritesh1603/DjangoDeploy.git'
    }

    stages {
        stage('Notify') {
          steps {
              script {
                  emailext(
                      subject: " Build for ${env.BRANCH_NAME} started",
                      body: "The Build proces for ${env.BRANCH_NAME} has been started. Check the status at url: $BUILD_URL ",
                      to: "cloudidpatil@gmail.com"
                    )
                }
            }
        }
        
        stage('Initialize') {
            steps {
                script {
                    env.DEPLOY_PATH = '/home/vagrant/staging/DjangoApp'
                }
            }
        }

        stage('Clone Repository') {
            steps {
                script {
                    git(
                        branch: env.BRANCH_NAME,
                        url: "${REPO_URL}",
                        credentialsId: 'github_token'
                    )
                }
            }
        }

        stage('Cache SSH Host Key') {
            steps {
                bat """
                echo y | "$PLINK_PATH" -pw "$DEPLOY_PASSWORD" "$DEPLOY_USER@$DEPLOY_HOST" exit
                """
            }
        }

        stage('Approval') {
          steps {
              script {
                  emailext(
                      subject: "Deployment Approval for ${env.BRANCH_NAME}",
                      body: " Please approve deployment for ${env.BRANCH_NAME} : $BUILD_URL ",
                      to: "cloudidpatil@gmail.com"
                    )
                  input(
                      id: 'userInput', message: 'Do you want to deploy to Staging?', ok: 'Deploy', submitter: 'rp_dev',
                      parameters: [
                          string(defaultValue: '', description: 'Please provide a reason for approval:', name: 'approvalReason')
                      ]
                  )
                }
            }
        }
        
        // stage('Run Ansible Playbook') {
        //     steps {
        //         bat """
        //         "$PLINK_PATH" -pw "$DEPLOY_PASSWORD" "$DEPLOY_USER@$DEPLOY_HOST" "ansible-playbook /home/vagrant/ansible_project/django/${env.BRANCH_NAME}-deployment-playbook.yml"
        //         """
        //     }
        // }
    }

    post {
        success {
            echo "Build and deployment for ${env.BRANCH_NAME} completed successfully."
        }
        failure {
            echo "Build and deployment for ${env.BRANCH_NAME} failed."
        }
    }
}
