terraform {

  # Configure the backend to use terraform remote for storing Terraform state
  backend "remote" {
    organization = "deora-devops"

    workspaces {
      name = "aws-devops"
    }
  }

  # This block is used to specify the providers and their versions
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">=1.2.0"
}

provider "aws" {
  region  = "eu-north-1"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket        = "anant-devops-iaac-tf-state" # REPLACE WITH YOUR BUCKET NAME
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "terraform_bucket_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_crypto_conf" {
  bucket        = aws_s3_bucket.terraform_state.bucket 
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}