# EC2-based Deployment with CodeDeploy

from aws_cdk import (
    Stack,
    aws_codedeploy as codedeploy,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling
)
from constructs import Construct

class DeployStack(Stack):
    def __init__(self, scope: Construct, id: str,
                 instance: ec2.Instance,
                 **kwargs):
        super().__init__(scope, id, **kwargs)

        # Tag instance so CodeDeploy can find it
        instance.instance.instance.add_property_override(
            "Tags", [{"Key": "Name", "Value": "FlaskAppEC2"}]
        )

        # Role for CodeDeploy
        codedeploy_role = iam.Role(
            self, "CodeDeployServiceRole",
            assumed_by=iam.ServicePrincipal("codedeploy.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodeDeployRole")
            ]
        )

        # Application
        self.application = codedeploy.ServerApplication(
            self, "FlaskAppDeployApp",
            application_name="FlaskAppEC2DeployApp"
        )

        # Deployment Group
        self.deployment_group = codedeploy.ServerDeploymentGroup(
            self, "FlaskAppDeployGroup",
            application=self.application,
            deployment_group_name="FlaskAppEC2Group",
            ec2_instance_tags=codedeploy.InstanceTagSet({
                "Name": ["FlaskAppEC2"]
            }),
            install_agent=True,
            deployment_config=codedeploy.ServerDeploymentConfig.ALL_AT_ONCE,
            role=codedeploy_role
        )
