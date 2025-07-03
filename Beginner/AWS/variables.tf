variable "aws_region" {
  description = "The AWS region to deploy the resources"
  default     = "eu-north-1"
}

variable "ecr_repository" {
  description = "The name of the ECR repository"
  default     = "dummy-demo-repo"
}

variable "container_image" {
  description = "ECR image URI"
  type        = string
#   default     = "dummy-demo-repo:latest"
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket for Terraform state"
  default     = "anant-devops-iaac-tf-state" # REPLACE WITH YOUR BUCKET NAME
}

variable "lambda_function_runtime" {
  description = "The runtime for the Lambda function"
  default     = "python3.9"
}

variable "terraform_organization" {
  description = "The Terraform Cloud organization name"
  default     = "deora-devops"
}

variable "terraform_workspace" {
  description = "The Terraform Cloud workspace name"
  default     = "aws-devops"
}