from aws_cdk import (
    Stack,
    aws_codebuild as codebuild,
    aws_iam as iam,
    aws_ecr as ecr,
    SecretValue,
)
from constructs import Construct

class CodeBuildStack(Stack):
    def __init__(self, scope: Construct, id: str, repo: ecr.Repository, **kwargs):
        super().__init__(scope, id, **kwargs)

        # IAM role for CodeBuild with permissions for ECR
        build_role = iam.Role(
            self, "CodeBuildRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com")
        )

        build_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryPowerUser")
        )
        build_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
        )

        # CodeBuild project
        self.project = codebuild.Project(
            self, "FlaskAppCodeBuild",
            source=codebuild.Source.git_hub(
                owner="anant16-devops",
                repo="aws-devops",
                branch_or_ref="main",
                oauth_token=SecretValue.secrets_manager("github-token"),
                clone_depth=1,
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_6_0,
                privileged=True  # Needed for Docker
            ),
            environment_variables={
                "REPOSITORY_URI": codebuild.BuildEnvironmentVariable(value=repo.repository_uri)
            },
            role=build_role,
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml")
        )

        # Grant permissions to allow pushing to ECR
        repo.grant_pull_push(self.project.role)
        # Output the CodeBuild project name
        self.project_name = self.project.project_name  # This can be used to reference the project
        self.repository = repo  # Store the repository reference for later use