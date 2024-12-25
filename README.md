## Flask Application with CI/CD using GitHub Actions, Docker & EC2

![ScreenShot Tool -20241225020132](https://github.com/user-attachments/assets/a60782a6-6b27-49ac-bf03-4edbe1983d3c)

##### Project Overview
- This project is a fully interactive Flask application, which is deployed using Continuous Integration and Continuous Deployment (CI/CD) workflows powered by GitHub Actions. The application is containerized using Docker, allowing for easy deployment to a remote EC2 instance. The workflow builds and pushes the Docker image to Docker Hub, then remotely deploys it on the EC2 instance for production.

Key Features:
-  Flask Application: A simple interactive web application built with Flask.
- CI/CD Pipeline: Automated deployment pipeline using GitHub Actions.
- Dockerized: Containerized application for easy deployment and scaling.
- Remote Deployment: Deployed to an EC2 instance using SSH commands.
- Floating Particles & Interactive UI: The webpage includes dynamic animations and an interactive button that triggers random messages.
### How It Works
##### 1. Flask Application:
- The Flask application is a simple web page that uses the Poppins font and provides an interactive button. When clicked, the button triggers a random message animation, while floating particles animate in the background.

Flask Code:
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
```
##### 2. Dockerization:
- The application is containerized using Docker. A Dockerfile is created to define the environment for the Flask application.

Example Dockerfile:
```dockerfile
-# Use Python image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy dependencies and application code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Expose port and run Flask app
EXPOSE 9000
CMD ["python", "app.py"]
```
##### 3. CI/CD with GitHub Actions:
- The CI/CD pipeline is powered by GitHub Actions. The workflow is triggered on every push to the main branch. The pipeline consists of the following steps:

- Checkout: Clone the repository.
- Docker Hub Login: Log in to Docker Hub using secrets.
- Build and Push: Build the Docker image and push it to Docker Hub.
- SSH Deployment: Use SSH to remotely deploy the Docker container to an EC2 instance.
#### GitHub Actions Workflow:
```yaml
name: Flask Application CI/CD

on:
  push:
    branches:
      - main

jobs:
  push_to_registry:
    name: Push Docker image to Docker Hub
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read
      attestations: write
      id-token: write
    steps:
      - name: Check out the repo
        uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@f4ef78c080cd8ba55a85445d5b36e214a81df20a
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@9ec57ed1fcdbf14dcef7dfbe97b2010124a938b7
        with:
          images: docker.io/r0han01/jenkins

      - name: Build and push Docker image
        id: push
        uses: docker/build-push-action@3b5e8027fcad23fda98b2e3ac259d8d67585f671
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

      - name: executing remote ssh commands using private key
        uses: appleboy/ssh-action@v1.2.0
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          port: ${{ secrets.PORT }}
          script: |
            docker stop jenkins || true
            docker rm jenkins || true
            docker rmi docker.io/r0han01/jenkins:main
            docker run --name jenkins -d -p 9000:9000 docker.io/r0han01/jenkins:main
```
##### 4. EC2 Deployment:
- Once the Docker image is pushed to Docker Hub, the GitHub Actions workflow uses SSH to connect to your EC2 instance, stop and remove any previous containers, and run the new container with the latest Docker image.

#### Setting Up Your Project
- Follow these steps to set up the application and CI/CD pipeline on your local machine and EC2 instance.

*Prerequisites:*
- Flask: Install Flask via pip install flask.
- Docker: Ensure Docker is installed and configured on your local machine and EC2 instance.
- GitHub Repository: Store your code in a GitHub repository.
Step 1: Clone the Repository
- Clone the repository to your local machine:
Step 2: Docker Setup
- Build and run the Docker container locally:
Step 3: Configure GitHub Actions Secrets
- To securely authenticate with Docker Hub and deploy to EC2, add the following secrets in your GitHub repository:

`DOCKER_USERNAME`
`DOCKER_PASSWORD`
`HOST (Your EC2 instance's IP address)`
`USERNAME (Your EC2 username)`
`SSH_PRIVATE_KEY (Your EC2 private SSH key)`
`PORT (The port for SSH connection, default is 22)`
Step 4: Deploy to EC2
- Once the GitHub Actions pipeline runs, your Docker container will be automatically deployed to your EC2 instance.

# Conclusion
- This project demonstrates how to build a simple Flask web application, Dockerize it, and deploy it using a CI/CD pipeline with GitHub Actions. By integrating Docker and EC2, we have created a scalable and automated deployment process for our application. The interactive webpage provides a fun and engaging user experience, while the CI/CD pipeline ensures that the latest changes are always deployed seamlessly.

Useful Links:
- https://jsonformatter.org/yaml-validator
- https://docs.github.com/en/actions/use-cases-and-examples/publishing-packages/publishing-docker-images
