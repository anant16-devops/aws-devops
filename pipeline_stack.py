# This pipeline will:
# Pull source code from GitHub
# Trigger the CodeBuild project (created in Step 3)
# (Optional later) Deploy the app to EC2 or ECS

from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    aws_codebuild as codebuild,
    aws_codedeploy as codedeploy,
    SecretValue
)
from constructs import Construct

class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str,
                 build_project: codebuild.IProject,
                 github_owner: str,
                 github_repo: str,
                 **kwargs):
        super().__init__(scope, id, **kwargs)

        # Artifacts
        source_output = codepipeline.Artifact()
        build_output = codepipeline.Artifact()

        # Pipeline
        pipeline = codepipeline.Pipeline(
            self, "FlaskAppPipeline",
            pipeline_name="FlaskAppDockerPipeline"
        )

        # Stage 1: Source from GitHub
        pipeline.add_stage(
            stage_name="Source",
            actions=[
                cpactions.GitHubSourceAction(
                    action_name="GitHub_Source",
                    owner=github_owner,
                    repo=github_repo,
                    branch="main",
                    oauth_token=SecretValue.secrets_manager("github-token"),
                    output=source_output
                )
            ]
        )

        # Stage 2: Build Docker and push to ECR
        pipeline.add_stage(
            stage_name="Build",
            actions=[
                cpactions.CodeBuildAction(
                    action_name="Docker_Build_and_Push",
                    project=build_project,
                    input=source_output,
                    outputs=[build_output]
                )
            ]
        )

        # Optionally, Stage 3: Deploy
        pipeline.add_stage(
            stage_name="Deploy",
            actions=[
                cpactions.CodeDeployServerDeployAction(
                    action_name="CodeDeploy_EC2",
                    deployment_group=codedeploy.ServerDeploymentGroup.from_server_deployment_group_attributes(
                        self, "ImportedDeployGroup",
                        application=codedeploy.ServerApplication.from_server_application_name(
                            self, "ImportedApp", "FlaskAppEC2DeployApp"
                        ),
                        deployment_group_name="FlaskAppEC2Group"
                    ),
                    input=build_output
                )
            ]
        )
        # You can add ECS deploy or CodeDeploy server deploy here later.
        # For now, we will just output the pipeline name
        self.pipeline_name = pipeline.pipeline_name  # This can be used to reference the pipeline later