pipeline {
    agent any
    //comment to check github webhook integration with jenkins 
    environment {
        DEPLOY_USER = 'vagrant'
        DEPLOY_HOST = '192.168.33.10'
        SSH_KEY = credentials('Fastapi_Vagrant')
        GITHUB_TOKEN = credentials('github_token')
        PLINK_PATH = 'C:\\Program Files\\PuTTY\\plink.exe'
        PSCP_PATH = 'C:\\Program Files\\PuTTY\\pscp.exe'
        DEPLOY_PASSWORD = 'vagrant'
        REPO_URL = 'https://github.com/ritesh1603/DjangoDeploy.git'
        JENKINS_USER = 'ritesh'
        API_TOKEN= '11f052970dbd36d531590ce20e8a401b4a'
    }
   
    stages {
         stage('Notify') {
             agent none
          steps {
              script {
                  emailext(
                      subject: " Build for ${env.BRANCH_NAME} started",
                      body: "The Build process for ${env.BRANCH_NAME} has been started. Check the status at url: $BUILD_URL/pipeline-console ",
                      to: "cloudidpatil@gmail.com"
                    )
                }
            }
        }
        
        stage('Initialize') {
            steps {
                script {
                    env.DEPLOY_PATH = '/home/vagrant/dev/DjangoApp'
                    env.BRANCH_TO_BUILD = 'uat'
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
        
        // stage('Run Ansible Playbook') {
        //     steps {
        //         bat """
        //         "$PLINK_PATH" -pw "$DEPLOY_PASSWORD" "$DEPLOY_USER@$DEPLOY_HOST" "ansible-playbook /home/vagrant/ansible_project/django/${env.BRANCH_NAME}-deployment-playbook.yml"
        //         """
        //     }
        // }

        stage('Approval') {
          steps {
              script {
                  emailext(
                      subject: "Deployment Approval for ${env.BRANCH_TO_BUILD}",
                      body: "The deployment for ${env.BRANCH_NAME} was successful. Please approve deployment for ${env.BRANCH_TO_BUILD} at url: $BUILD_URL/pipeline-console ",
                      to: "cloudidpatil@gmail.com"
                    )
                  def approvalGiven = false
                  while(!approvalGiven)
                  {
                      try {
                      def approval = input(
                      id: 'userInput', message: 'Do you want to deploy to UAT?', ok: 'Deploy', submitterParameter: 'submitter',
                      parameters: [
                          string(defaultValue: '', description: 'Please provide a reason for approval:', name: 'approvalReason')
                      ]
                      )
                      approvalGiven=checkUserRole(approval.submitter, 'devops')
                      if (!approvalGiven) {
                          echo "You need to be part of devops role to submit this. Please try again."
                      }
                      }catch (Exception e)
                      {

                          def abortsignal=checkUserRole(approval.submitter, 'devops')
                          if(abortsignal)
                          {
                              error("deployment aborted by devops member ${approval.submitter} due to ${approval.approvalReason}) 
                          }
                          else
                          {
                              echo "Abort attempt by non devops member ${approval.submitter}!"
                          }
                      }
                  }
                  // if (!checkUserRole(approval.submitter, 'devops')) {
                  //       error("You need to be part of devops role to submit this.")
                  //   }
                }
            }
        }
        
        stage('Notify and Trigger Next Build') {
            steps {
                script {
                    build(job: "MultiBranchDeployment_Django1" + "/" + "${env.BRANCH_TO_BUILD}".replaceAll('/', '%2F'))
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

def checkUserRole(userId, requiredRole) {
    def roleStr = roleStr = bat(script: """
            curl -s -u "$JENKINS_USER:$API_TOKEN" ^
            "%JENKINS_URL%/user/${userId}/roles"
            """, returnStdout: true).trim()
    return roleStr.contains(requiredRole)
}
