from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    aws_apigateway as apigateway,
    aws_lambda_python_alpha as lambda_alpha_,
    aws_lambda as _lambda,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_events as events, 
    aws_events_targets as events_targets,

)

from types import SimpleNamespace

class RNADashboardStack(Stack):
    def __init__(self, 
                 scope: Construct, 
                 construct_id: str, 
                 cfg: SimpleNamespace, 
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##################### MAP DATA BUCKET #####################
        bucket_name=cfg.bucket_name 
        folder_to_deploy = "rna_dashboard/data/www"

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

        # #FIXME: need to refactor all this for Fargate
        # ##################### WWW HANDLER LAMBDA #####################
        # my_handler = lambda_alpha_.PythonFunction(
        #     self,
        #     "RNA_Dashboard_WWW_Lambda",
        #     entry="./rna_dashboard/functions/www/",
        #     index="app.py",
        #     handler="handler",
        #     timeout=Duration.seconds(60),
        #     runtime=_lambda.Runtime.PYTHON_3_8,
        #     memory_size=10240,
        #     environment={"BUCKET_NAME": cfg.bucket_name,
        #                  "BUCKET_URL": f"https://{cfg.bucket_name}.s3.{cfg.region}.amazonaws.com"
        #                  }
        # )

        # my_handler.node.add_dependency(deployment)


        #FIXME: need to refactor all this for Fargate
        # ##################### REST API GATEWAY WITH CUSTOM DOMAIN #####################

        # root_domain = cfg.domain
        # subdomain = cfg.subdomain
        # fully_qualified_domain_name = f"{subdomain}.{root_domain}"

        # # get the hosted zone
        # my_hosted_zone = route53.HostedZone.from_lookup(
        #     self, "BusObservatoryAPI_HostedZone", domain_name=root_domain
        # )

        # # create certificate
        # my_certificate = acm.Certificate(
        #     self,
        #     "RNA_Dashboard_Stack_Certificate",
        #     domain_name=fully_qualified_domain_name,
        #     validation=acm.CertificateValidation.from_dns(hosted_zone=my_hosted_zone),
        # )

        # # export the certificate arn
        # self.certificate_arn = my_certificate.certificate_arn

        # # create REST API
        # my_api = apigateway.LambdaRestApi(
        #     self,
        #     "RNA_Dashboard_WWW_ApiGateway",
        #     handler=my_handler,
        #     domain_name=apigateway.DomainNameOptions(
        #         domain_name=fully_qualified_domain_name,
        #         certificate=my_certificate,
        #         security_policy=apigateway.SecurityPolicy.TLS_1_2,
        #         endpoint_type=apigateway.EndpointType.EDGE,
        #     ),
        # )

        # # create DNS A record
        # route53.ARecord(
        #     self,
        #     "RNA_Dashboard__WWW_ApiRecord",
        #     record_name=subdomain,
        #     zone=my_hosted_zone,
        #     target=route53.RecordTarget.from_alias(targets.ApiGateway(my_api)),
        # )


        #FIXME: chatgpt starter for Fargate
        '''
        from aws_cdk import core
        import aws_cdk.aws_ec2 as ec2
        import aws_cdk.aws_ecs as ecs
        import aws_cdk.aws_elasticloadbalancingv2 as elbv2
        import aws_cdk.aws_logs as logs
        import aws_cdk.aws_iam as iam
        import aws_cdk.aws_secretsmanager as sm


        class FlaskFargateStack(core.Stack):

            def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
                super().__init__(scope, id, **kwargs)

                # Create a VPC for the Fargate cluster
                vpc = ec2.Vpc(self, "FlaskFargateVpc",
                            max_azs=2,
                            nat_gateways=1)

                # Create a Fargate cluster in the VPC
                cluster = ecs.Cluster(self, "FlaskFargateCluster",
                                    vpc=vpc)

                # Create a Fargate task definition for the Flask app
                task_definition = ecs.FargateTaskDefinition(self, "FlaskFargateTask",
                                                            memory_limit_mib=512,
                                                            cpu=256)

                # Add a container to the task definition for the Flask app
                container = task_definition.add_container("FlaskFargateContainer",
                                                        image=ecs.ContainerImage.from_registry("public.ecr.aws/some-repo/flask-app"),
                                                        environment={
                                                            "SECRET_KEY": sm.Secret.from_secret_name_v2(
                                                                self, "FlaskFargateSecret", "flask-app-secret").secret_value.to_string(),
                                                            "DATABASE_URL": "postgresql://user:password@database:5432/db"
                                                        })

                # Add port mappings for the container
                container.add_port_mappings(ecs.PortMapping(container_port=5000))

                # Create a service for the task definition
                service = ecs.FargateService(self, "FlaskFargateService",
                                            cluster=cluster,
                                            task_definition=task_definition,
                                            desired_count=2)

                # Create a load balancer for the service
                lb = elbv2.ApplicationLoadBalancer(self, "FlaskFargateLb",
                                                    vpc=vpc,
                                                    internet_facing=True)

                listener = lb.add_listener("FlaskFargateListener",
                                            port=80,
                                            open=True)

                # Create a target group for the service
                target_group = elbv2.ApplicationTargetGroup(self, "FlaskFargateTargetGroup",
                                                            port=5000,
                                                            vpc=vpc,
                                                            health_check=elbv2.HealthCheck(interval=core.Duration.seconds(30)))

                # Register the service with the target group
                target_group.add_targets("FlaskFargateTarget",
                                        port=5000,
                                        targets=[service])

                # Add the target group to the load balancer listener


        '''