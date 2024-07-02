pipeline {
    agent any

    environment {
        DEPLOY_USER = 'vagrant'
        DEPLOY_HOST = '192.168.33.10'
        SSH_KEY = credentials('Fastapi_Vagrant')
        GITHUB_TOKEN = credentials('github_token')
        PLINK_PATH = 'C:\\Program Files\\PuTTY\\plink.exe'
        PSCP_PATH = 'C:\\Program Files\\PuTTY\\pscp.exe'
        DEPLOY_PASSWORD = 'vagrant'
        REPO_URL = 'https://github.com/ritesh1603/DjangoDeploy.git'
        SONARQUBE_SERVER = 'https://02f3-104-28-211-36.ngrok-free.app/'
        SONARQUBE_TOKEN = credentials('Sonar_jenkins')
        SONAR_SCANNER_PATH = 'D:\\Downloads\\sonar-scanner-cli-6.0.0.4432-windows\\sonar-scanner-6.0.0.4432-windows\\bin'
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    env.DEPLOY_PATH = '/home/vagrant/uat/DjangoApp'
                    env.BRANCH_TO_BUILD = 'staging'
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
        // stage('Approval') {
        //   steps {
        //       script {
        //           def userInput = input(
        //               id: 'userInput', message: 'Do you want to deploy to Staging?', ok: 'Deploy',
        //               parameters: [
        //                   string(defaultValue: '', description: 'Please provide a reason for approval:', name: 'approvalReason')
        //               ]
        //           )
        //           emailext(
        //               subject: "Deployment Approval for ${env.BRANCH_NAME}",
        //               body: "The deployment for ${env.BRANCH_NAME} has been approved with the following reason: ${userInput}",
        //               recipientProviders: [[$class: 'DevelopersRecipientProvider']]
        //             )
        //         }
        //     }
        // }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube_Server') { 
                    bat """
                    SET PATH=${SONAR_SCANNER_PATH};%PATH%
                    sonar-scanner -Dsonar.projectKey=sonar-project2 -Dsonar.sources=. -Dsonar.host.url=${SONARQUBE_SERVER} -Dsonar.login=${SONARQUBE_TOKEN}
                    """
                }
            }
        }

        
        stage('Run Ansible Playbook') {
            steps {
                bat """
                "$PLINK_PATH" -pw "$DEPLOY_PASSWORD" "$DEPLOY_USER@$DEPLOY_HOST" "ansible-playbook /home/vagrant/ansible_project/django/${env.BRANCH_NAME}-deployment-playbook.yml"
                """
            }
        }

        


        stage('Notify and Trigger Next Build') {
            steps {
                script {
                    build(job: "MultiBranchDeployment_Django2" + "/" + "${env.BRANCH_TO_BUILD}".replaceAll('/', '%2F'))
                }
            }
        }
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
