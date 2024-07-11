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
        SONARQUBE_SERVER = 'http://192.168.33.11:9000/'
        SONARQUBE_TOKEN = credentials('Sonar_jenkins')
        SONAR_SCANNER_PATH = 'D:\\Downloads\\sonar-scanner-cli-6.0.0.4432-windows\\sonar-scanner-6.0.0.4432-windows\\bin'
        VERSION_NUMBER= 'v1.1'
    }

    stages {
        
        stage('Notify') {
          steps {
              script {
                  emailext(
                      subject: "Build for ${env.BRANCH_NAME} started",
                      body: "The Build process for ${env.BRANCH_NAME} has been started. Check the status at url: $BUILD_URL ",
                      to: "cloudidpatil@gmail.com"
                    )
                }
            }
        }
        
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

        // stage('Cache SSH Host Key') {
        //     steps {
        //         bat """
        //         echo y | "$PLINK_PATH" -pw "$DEPLOY_PASSWORD" "$DEPLOY_USER@$DEPLOY_HOST" exit
        //         """
        //     }
        // }
        stage('Run Unit Tests') {
            steps {
                bat """
                pip install django django-debug-toolbar
                python manage.py migrate
                python manage.py test
                """
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube_Server') { 
                    bat """
                    SET PATH=${SONAR_SCANNER_PATH};%PATH%
                    sonar-scanner -Dsonar.projectKey=sonar-project2 -Dsonar.sources=. -Dsonar.host.url=${SONARQUBE_SERVER} -Dsonar.login=${SONARQUBE_TOKEN} -X
                    """
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
        stage('Tag Branch') {
            steps {
                    bat """
                    git tag ${VERSION_NUMBER}
                    git push origin ${VERSION_NUMBER}
                    """
            }
        }
        stage('Approval') {
          steps {
              script {
                  emailext(
                      subject: "Deployment Approval for ${env.BRANCH_TO_BUILD}",
                      body: "The Deployment for ${env.BRANCH_NAME} was successful. Please approve deployment for ${env.BRANCH_TO_BUILD} : $BUILD_URL ",
                      to: "cloudidpatil@gmail.com"
                    )
                  def approval = input(
                      id: 'userInput', message: 'Do you want to deploy to staging?', ok: 'Deploy', submitter: 'rp_devops,rp_devops2', submitterParameter:’submitter’,
                      parameters: [
                          string(defaultValue: '', description: 'Please provide a reason for approval:', name: 'approvalReason')
                      ]
                  )
                   echo "Approval given by ${approval.submitter} due to ${approval['approvalReason']}"

                }
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
