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
        instance.instance.add_property_override(
            "Tags", [{"Key": "Name", "Value": "FlaskAppEC2"}]
        )

        # Role for CodeDeploy
        codedeploy_role = iam.Role(
            self, "CodeDeployServiceRole",
            assumed_by=iam.ServicePrincipal("codedeploy.amazonaws.com")
            )
        #     managed_policies=[
        #         iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodeDeployRole")
        #     ]
        # )
        # codedeploy_role = "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole"

        # Application
        codedeploy_app = codedeploy.ServerApplication(
            self, "FlaskAppDeployApp",
            application_name="FlaskAppEC2DeployApp"
        )

        # Deployment Group
        codedeploy_group = codedeploy.ServerDeploymentGroup(
            self, "FlaskAppDeployGroup",
            application=codedeploy_app,
            deployment_group_name="FlaskAppEC2Group",
            ec2_instance_tags=codedeploy.InstanceTagSet({
                "Name": ["FlaskAppEC2"]
            }),
            install_agent=True,
            deployment_config=codedeploy.ServerDeploymentConfig.ALL_AT_ONCE,
            role=codedeploy_role
        )

        self.codedeploy_app = codedeploy_app
        self.codedeploy_group = codedeploy_group
