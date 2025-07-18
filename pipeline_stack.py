# This pipeline will:
# Pull source code from GitHub
# Trigger the CodeBuild project (created in Step 3)
# (Optional later) Deploy the app to EC2 or ECS

from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_iam as iam, aws_ecr as ecr,
    SecretValue
)

from constructs import Construct


class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str,
                 github_owner: str,
                 github_repo: str,
                 repository_name,
                 code_deploy_group,
                 **kwargs):
        super().__init__(scope, id, **kwargs)

        # Ensure the S3 bucket exists
        artifacts_bucket = s3.Bucket(
            self, "ArtifactsBucket", versioned=True)
        
        build_role = iam.Role(
            self, "CodeBuildRole",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com")
        )

        build_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryPowerUser")
        )
        build_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )


        # Create CodeBuild project in the same stack
        codebuild_project = codebuild.Project(
            self, "FlaskAppDockerBuild",
            role=build_role,
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            source=codebuild.Source.git_hub(
                owner=github_owner,
                repo=github_repo
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_7_0,
                privileged=True,  # Required for Docker builds
                compute_type=codebuild.ComputeType.SMALL
            ),
            environment_variables={
                "AWS_DEFAULT_REGION": codebuild.BuildEnvironmentVariable(
                    value=self.region
                ),
                "AWS_ACCOUNT_ID": codebuild.BuildEnvironmentVariable(
                    value=self.account
                ),
                "REPOSITORY_URI": codebuild.BuildEnvironmentVariable(
                    value=f"{self.account}.dkr.ecr.{self.region}.amazonaws.com/{repository_name}"
                )
            },
            artifacts=codebuild.Artifacts.s3(
                bucket=artifacts_bucket,
                path="build-artifacts"
            )
        )
        
        # Artifacts
        source_output = codepipeline.Artifact("SourceOutput")
        build_output = codepipeline.Artifact("BuildOutput")

        # Pipeline
        pipeline = codepipeline.Pipeline(
            self, "FlaskAppPipeline",
            pipeline_name="FlaskAppDockerPipeline",
            artifact_bucket=artifacts_bucket,
        )

        # Stage 1: Source from GitHub
        pipeline.add_stage(
            stage_name="Source",
            actions=[
                codepipeline_actions.GitHubSourceAction(
                    action_name="GitHub_Source",
                    owner=github_owner,
                    repo=github_repo,
                    output=source_output,
                    branch="main",
                    oauth_token=SecretValue.secrets_manager("my-github-token"),
                    )
            ]
        )
        # Stage 2: Build Docker and push to ECR
        pipeline.add_stage(
            stage_name="Build",
            actions=[
                codepipeline_actions.CodeBuildAction(
                    action_name="Docker_Build_and_Push",
                    project=codebuild_project,
                    input=source_output,
                    outputs=[build_output]
                )
            ]
        )
        # Optionally, Stage 3: Deploy
        pipeline.add_stage(
            stage_name="Deploy",
            actions=[
                codepipeline_actions.CodeDeployServerDeployAction(
                    action_name="CodeDeploy_EC2",
                    deployment_group=code_deploy_group,
                    input=build_output
                )
            ]
        )
        # You can add ECS deploy or CodeDeploy server deploy here later.
        # For now, we will just output the pipeline name
        self.pipeline_name = pipeline.pipeline_name  # This can be used to reference the pipeline later