from constructs import Construct
from aws_cdk import (
    Stack,
    Tag,
    aws_cloudfront as cf,
    custom_resources as cr,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,


)

from types import SimpleNamespace

class RNADashboardStack(Stack):
    def __init__(self, 
                 scope: Construct, 
                 construct_id: str, 
                 cfg: SimpleNamespace, 
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        tag = Tag("project", cfg.project)

        #TODO render static site
        # https://arunkprasad.com/log/how-to-create-a-static-website-with-flask/

       ##################### MAP DATA BUCKET #####################
        #TODO: create S3 bucket from build folder
        #TODO: add S3 deployment


        bucket_name=cfg.stack_name 
        folder_to_deploy = "app/build"

        bucket = s3.Bucket(self,
            f"{cfg.stack_name}__Data_Bucket",
            bucket_name=bucket_name,
            public_read_access=True,
        )

        deployment = s3_deployment.BucketDeployment(self, 
            f"{cfg.stack_name}__Data_Bucket_Deployment",
            sources=[s3_deployment.Source.asset(folder_to_deploy)],
            destination_bucket=bucket,
            # memory_limit=1024,
        )


        # #TODO: create CloudFront distribution
        # # https://rubenjgarcia.cloud/static-web-in-cloudfront-with-aws-cdk/


        # parameter = cr.AwsCustomResource(self, "GetCertificateArn",
        #                             on_update=cr.AwsSdkCall(
        #                                 service="SSM",
        #                                 action="getParameter",
        #                                 parameters={
        #                                     "Name": "certificate-arn"
        #                                 },
        #                                 region="us-east-1",
        #                                 physical_resource_id=str(time.time)
        #                             )
        #                             )
 
        # cf.CloudFrontWebDistribution(self, "CDN",
        #                              price_class=cf.PriceClass.PRICE_CLASS_100,
        #                              alias_configuration=cf.AliasConfiguration(
        #                                  names=["static.rubenjgarcia.es"],
        #                                  acm_cert_ref=parameter.get_data_string("Parameter.Value"),
        #                                  ssl_method=cf.SSLMethod.SNI,
        #                                  security_policy=cf.SecurityPolicyProtocol.TLS_V1_1_2016
        #                              ),
        #                              origin_configs=[
        #                                  cf.SourceConfiguration(
        #                                      behaviors=[
        #                                          cf.Behavior(
        #                                              is_default_behavior=True)
        #                                      ],
        #                                      s3_origin_source=cf.S3OriginConfig(
        #                                          s3_bucket_source=bucket
        #                                      )
        #                                  )
        #                              ]
        #                              )


        # ##################### CUSTOM DOMAIN #####################

        # root_domain = cfg.domain
        # subdomain = cfg.subdomain
        # fully_qualified_domain_name = f"{subdomain}.{root_domain}"

        # # get the hosted zone
        # zone = route53.HostedZone.from_lookup(
        #     self, 
        #     f"{cfg.stack_name}__HostedZone", 
        #     domain_name=root_domain
        # )

        # # Create an ACM certificate for the domain
        # certificate = acm.Certificate(
        #     self, f"{cfg.stack_name}__FlaskFargateCertificate",
        #     domain_name=fully_qualified_domain_name,
        #     validation=acm.CertificateValidation.from_dns(zone))

        # # Create an A record in the Route 53 hosted zone to point to the Fargate service
        # route53.ARecord(
        #     self, f"{cfg.stack_name}__FlaskFargateRecord",
        #     zone=zone,
        #     record_name=subdomain,
        #     target=route53.RecordTarget.from_ip_addresses(*service.load_balancer.load_balancer_dns_names)
        #     )


