from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class NetworkStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create a VPC with 1 public subnet
        self.vpc = ec2.Vpc(
            self, "AppVPC",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC
                )
            ]
        )

        # Security group
        self.sg = ec2.SecurityGroup(
            self, "AppSG",
            vpc=self.vpc,
            description="Allow SSH and HTTP",
            allow_all_outbound=True
        )
        self.sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH Access")
        self.sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP Access")

        # IAM role for EC2 instance
        self.role = iam.Role(
            self, "EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        self.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryReadOnly")
        )
        self.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )

        # Amazon Linux 2 AMI with Docker
        ami = ec2.MachineImage.latest_amazon_linux()

        # EC2 instance
        self.instance = ec2.Instance(
            self, "AppInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ami,
            vpc=self.vpc,
            security_group=self.sg,
            role=self.role
        )
        # User data to install Docker and run the container
        self.instance.user_data.add_commands(
            "yum update -y",
            "amazon-linux-extras install docker -y",
            "service docker start",
            "usermod -a -G docker ec2-user",
            "docker pull 837217115905.dkr.ecr.eu-north-1.amazonaws.com/my-flask-app:latest",
            "docker run -d -p 80:80 837217115905.dkr.ecr.eu-north-1.amazonaws.com/my-flask-app:latest"
        )