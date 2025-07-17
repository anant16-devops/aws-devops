# File: app.py
# This code initializes the AWS CDK application and creates an instance of the NetworkStack.
# The NetworkStack is defined in the network_stack.py file, which sets up the VPC, security group, IAM role, and EC2 instance with Docker installed.
# The `env` parameter specifies the AWS account and region where the stack will be deployed. 
# The `app.synth()` method synthesizes the CloudFormation template from the defined stack.

import aws_cdk as cdk
from network_stack import NetworkStack
from ecr_stack import EcrStack
from codebuild_stack import CodeBuildStack
from pipeline_stack import PipelineStack
from deploy_stack import DeployStack

app = cdk.App()

network_stack = NetworkStack(app, "NetworkStack", env=cdk.Environment(account="837217115905", region="eu-north-1"))

ecr_stack = EcrStack(app, "EcrStack", env=cdk.Environment(account="837217115905", region="eu-north-1"))

codebuild_stack = CodeBuildStack(app, "CodeBuildStack", repo=ecr_stack.repository, env=cdk.Environment(account="837217115905", region="eu-north-1"))

codepipeline_stack = PipelineStack(app, "PipelineStack", build_project=codebuild_stack.project,
    github_owner="anant16-devops",
    github_repo="aws-devops",
    env=cdk.Environment(account="837217115905", region="eu-north-1")
)

deploy_stack = DeployStack(app, "DeployStack", instance=network_stack.instance, env=cdk.Environment(account="837217115905", region="eu-north-1"))

app.synth()