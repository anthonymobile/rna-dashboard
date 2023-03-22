from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    Tag,
    aws_apigateway as apigateway,
    aws_lambda_python_alpha as lambda_alpha_,
    aws_lambda as _lambda,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,

)
import os
from types import SimpleNamespace

class RNADashboardStack(Stack):
    def __init__(self, 
                 scope: Construct, 
                 construct_id: str, 
                 cfg: SimpleNamespace, 
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        ##################### TAG ALL STACK RESOURCES #####################
        tag = Tag("project", cfg.project)

        ##################### MAP DATA BUCKET #####################
        bucket_name=cfg.bucket_name 
        folder_to_deploy = "rna_dashboard/app/templates"

        bucket = s3.Bucket(self,
            f"{cfg.stack_name}__Data_Bucket",
            bucket_name=bucket_name,
            public_read_access=True,
        )

        deployment = s3deploy.BucketDeployment(self, 
            f"{cfg.stack_name}__Data_Bucket_Deployment",
            sources=[s3deploy.Source.asset(folder_to_deploy)],
            destination_bucket=bucket,
            # memory_limit=1024,
        )
