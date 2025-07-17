# aws-devops

## This repository explores the CI/CD & IaaC with AWS services like CodeBuild, CodeDeploy, CodePipeline and AWS CDK (python) for the purpose creating application infrastructure.

## Following is the directory structure of the repository:

Full AWS CDK pipeline, which:

Provisions infrastructure (VPC, EC2, ECR)

Builds Docker images via CodeBuild

Automates CI/CD via CodePipeline

Deploys to EC2 using CodeDeploy with appspec hooks

my-flask-deploy-cdk/
├── app.py                             # CDK entry point
├── buildspec.yml                      # Tells CodeBuild how to build & push Docker image
├── appspec.yml                        # Tells CodeDeploy how to deploy to EC2
├── cdk.json
├── requirements.txt                   # Python dependencies (CDK libs)
│
├── scripts/                           # Deployment lifecycle scripts
│   ├── start.sh
│   └── stop.sh
│
├── app/                               # Flask + Gunicorn app
│   ├── main.py
│   ├── wsgi.py
│   └── requirements.txt
│
├── nginx/                             # NGINX config
│   └── nginx.conf
│
├── Dockerfile                         # Builds Flask + Gunicorn + NGINX container
│
├── network_stack.py                   # VPC, EC2, Security Group
├── ecr_stack.py                       # ECR repo for Docker images
├── codebuild_stack.py                 # CodeBuild project for building/pushing Docker
├── pipeline_stack.py                  # CodePipeline stages (source, build, deploy)
├── deploy_stack.py                    # CodeDeploy setup for EC2


📦 Inside Each File/Dir:

File/Folder	        Purpose
app.py	            Orchestrates CDK app stacks
network_stack.py	VPC, EC2 instance, SG, IAM for EC2
ecr_stack.py	    Private ECR repo for Docker image
codebuild_stack.py	CodeBuild project pulling from GitHub and pushing to ECR
pipeline_stack.py	CodePipeline setup: Source → Build → Deploy
deploy_stack.py	    CodeDeploy application + deployment group
Dockerfile	        Docker container image (Python + Flask + Gunicorn + NGINX)
buildspec.yml	    Docker build + push instructions for CodeBuild
appspec.yml	        CodeDeploy install/start hooks
scripts/	        Lifecycle shell scripts used in appspec (start/stop Docker)
app/	            Your Python Flask app
nginx/	            Reverse proxy config for NGINX