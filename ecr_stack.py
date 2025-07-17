from aws_cdk import (
    Stack,
    aws_ecr as ecr
)
from constructs import Construct

class EcrStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create an ECR repository
        self.repository = ecr.Repository(
            self, "FlaskAppRepo",
            repository_name="flask-nginx-app",
            removal_policy=None  # Use DESTROY for cleanup during testing
        )
        # Output the repository URI
        self.repository_uri = self.repository.repository_uri # This will be used to push the Docker image