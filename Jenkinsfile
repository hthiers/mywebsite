pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        IMAGE_NAME = 'portfolio-website'
        CONTAINER_NAME = 'portfolio'
        DATA_VOLUME = 'portfolio-data'

        // Credentials from Jenkins
        DOCKER_CREDENTIALS = credentials('docker-registry-credentials')
        SECRET_KEY = credentials('portfolio-secret-key')
        ADMIN_USERNAME = credentials('portfolio-admin-username')
        ADMIN_PASSWORD_HASH = credentials('portfolio-admin-password-hash')

        // SSH credentials
        DEPLOY_HOST = credentials('deploy-host')
        SSH_CREDENTIALS = credentials('deploy-ssh-credentials')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo '🏗️ Building Docker image...'

                    // Build the image
                    docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                    docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:latest")
                }
            }
        }

        stage('Test Image') {
            steps {
                script {
                    echo '🧪 Testing Docker image...'

                    // Run basic health check
                    sh """
                        docker run --rm ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} \
                            python -c "from database import init_db; print('✓ Database module OK')"
                    """
                }
            }
        }

        stage('Push to Registry') {
            steps {
                script {
                    echo '📤 Pushing to Docker registry...'

                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                        def image = docker.image("${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }

        stage('Deploy to Server') {
            steps {
                script {
                    echo '🚀 Deploying to production server...'

                    sshagent(credentials: ['deploy-ssh-credentials']) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ${DEPLOY_HOST} << 'EOF'
                                set -e

                                echo "Logging into registry..."
                                echo "${DOCKER_CREDENTIALS_PSW}" | docker login ${DOCKER_REGISTRY} -u ${DOCKER_CREDENTIALS_USR} --password-stdin

                                echo "Pulling latest image..."
                                docker pull ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest

                                echo "Creating volume if needed..."
                                docker volume create ${DATA_VOLUME} || true

                                echo "Stopping existing container..."
                                docker stop ${CONTAINER_NAME} || true
                                docker rm ${CONTAINER_NAME} || true

                                echo "Starting new container..."
                                docker run -d \
                                  --name ${CONTAINER_NAME} \
                                  --restart unless-stopped \
                                  -p 8080:8080 \
                                  -e SECRET_KEY="${SECRET_KEY}" \
                                  -e ADMIN_USERNAME="${ADMIN_USERNAME}" \
                                  -e ADMIN_PASSWORD_HASH="${ADMIN_PASSWORD_HASH}" \
                                  -e FLASK_ENV=production \
                                  -v ${DATA_VOLUME}:/app/data \
                                  ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest

                                echo "Waiting for health check..."
                                sleep 10

                                echo "Verifying deployment..."
                                docker exec ${CONTAINER_NAME} python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/articles')"

                                echo "Cleaning up old images..."
                                docker image prune -f

                                echo "✅ Deployment successful!"
EOF
                        """
                    }
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    echo '🏥 Performing health check...'

                    sshagent(credentials: ['deploy-ssh-credentials']) {
                        sh """
                            ssh ${DEPLOY_HOST} \
                                'docker exec ${CONTAINER_NAME} python -c "import urllib.request; urllib.request.urlopen(\"http://localhost:8080/api/articles\")"'
                        """
                    }

                    echo '✅ Health check passed!'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'

            // Notify success (customize with your notification method)
            // slackSend(color: 'good', message: "Deployment successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
            // emailext(subject: "Deployment Success", body: "Portfolio website deployed successfully")
        }

        failure {
            echo '❌ Pipeline failed!'

            // Notify failure
            // slackSend(color: 'danger', message: "Deployment failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
            // emailext(subject: "Deployment Failed", body: "Portfolio website deployment failed")
        }

        always {
            // Cleanup
            echo '🧹 Cleaning up...'
            sh 'docker system prune -f || true'
        }
    }
}
