from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
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

        ##################### BUCKET #####################
        bucket_name=cfg.bucket_name 

        bucket = s3.Bucket(self,
            f"{cfg.stack_name}__Data_Bucket",
            bucket_name=bucket_name,
            public_read_access=True,
        )

        ##################### CERTIFICATE #####################
        root_domain = cfg.domain
        subdomain = cfg.subdomain
        fully_qualified_domain_name = f"{subdomain}.{root_domain}"

        zone = route53.HostedZone.from_lookup(
            self, 
            f"{cfg.stack_name}__HostedZone", 
            domain_name=root_domain
        )
        
        certificate = acm.Certificate(
            self, f"{cfg.stack_name}__Certificate",
            domain_name=fully_qualified_domain_name,
            validation=acm.CertificateValidation.from_dns(zone))
        

        ##################### CLOUDFRONT #####################

        distribution = cloudfront.CloudFrontWebDistribution(
            self, 
            "MyDistribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=bucket
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            is_default_behavior=True,
                            default_ttl=Duration.seconds(60),
                        )
                    ],
                )
            ],
            viewer_certificate=cloudfront.ViewerCertificate.from_acm_certificate(
                certificate=certificate,
                aliases=[fully_qualified_domain_name],
                security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1_1_2016,  # default
                ssl_method=cloudfront.SSLMethod.SNI
                )
        )

        distribution.node.add_dependency(certificate)
        # distribution.node.add_dependency(deployment)

        # #TODO figure out how to run freeze
        # #FIXME 500 INTERNAL SERVER ERROR
        # # ##################### BUILD THE SITE #####################
        # # # importing doesnt seem to work because the modules dont import correctly
        # import subprocess
        # subprocess.run(['python', './rna_dashboard/app/freeze.py'])


        # ##################### CLOUDFRONT MODERN #####################
        # # more modern but if it ain't broke don't fix it
        # # Create a CloudFront distribution and map it to your custom domain
        # distribution = cloudfront.Distribution(
        #     self,
        #     "MyDistribution",
        #     default_behavior=cloudfront.BehaviorOptions(
        #         origin=cloudfront.S3OriginConfig(
        #             s3_bucket_source=bucket,
        #         ),
        #         cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
        #         viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        #     ),
        #     certificate=cloudfront.Certificate.from_acm_certificate(
        #         acm_certificate=core.SecretValue.secrets_manager(
        #             "my/acm/cert", json_field="arn"
        #         ),
        #     ),
        #     domain_names=["example.com", "www.example.com"],
        # )


        ##################### CONTENT DEPLOYMENT #####################

        folder_to_deploy = "site_staging"
        deployment = s3deploy.BucketDeployment(self, 
            f"{cfg.stack_name}__Data_Bucket_Deployment",
            sources=[s3deploy.Source.asset(folder_to_deploy)],
            destination_bucket=bucket,
            distribution=distribution,
            distribution_paths=["/*"], #invalidate all paths
            memory_limit=1024, #without this it will just hang and not deploy with no error
        )



        ##################### DNS A RECORD #####################

        route53.ARecord(
            self, 
            "AliasRecord",
            zone=zone,
            record_name=subdomain,
            target=route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(distribution)
            ),
        )
