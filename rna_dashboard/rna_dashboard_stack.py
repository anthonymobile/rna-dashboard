from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    Tag,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_cloudfront as cloudfront,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
)

from types import SimpleNamespace

class RNADashboardStack(Stack):
    def __init__(self, 
                 scope: Construct, 
                 construct_id: str, 
                 cfg: SimpleNamespace, 
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       ##################### LOAD CONFIG #####################
        tag = Tag("project", cfg.project)

        # #FIXME this wont render static site because it cant import Maps in the subfolder
        # # https://arunkprasad.com/log/how-to-create-a-static-website-with-flask/
        # # not sure how to run app/freeze.py
        # from flask_frozen import Freezer
        # from rna_dashboard.app.app import app
        # freezer = Freezer(app)
        # app.config['FREEZER_BASE_URL'] = "http://localhost:5000" # not fully_qualified_domain_name?
        # freezer.freeze()

        #MANUAL BUILD
        # cd rna-dashboard
        # source .venv/bin/activate
        # cd rna_dashboard/app
        # python freeze.py


        ##################### STATIC SITE #####################
        bucket_name=cfg.stack_name 
        folder_to_deploy = "rna_dashboard/app/build"

        # https://pypi.org/project/aws-cdk.aws-s3-deployment/
        website_bucket = s3.Bucket(
            self, 
            f"{cfg.stack_name}__Data_Bucket",
            bucket_name=bucket_name,
            website_index_document="index.html",
            public_read_access=True
        )

        s3deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3deploy.Source.asset(folder_to_deploy)],
            destination_bucket=website_bucket,
            # destination_key_prefix="web/static"
        )

        # ##################### CERTIFICATE #####################
        # root_domain = cfg.domain
        # subdomain = cfg.subdomain
        # fully_qualified_domain_name = f"{subdomain}.{root_domain}"

        # # get the hosted zone
        # zone = route53.HostedZone.from_lookup(
        #     self, 
        #     f"{cfg.stack_name}__HostedZone", 
        #     domain_name=root_domain
        # )
        
        # certificate = acm.Certificate(
        #     self, f"{cfg.stack_name}__FlaskFargateCertificate",
        #     domain_name=fully_qualified_domain_name,
        #     validation=acm.CertificateValidation.from_dns(zone))
        
        # #TODO more modern distribution construct
        # # ##################### CLOUDFRONT MODERN #####################
        # # # Create a CloudFront distribution and map it to your custom domain
        # # distribution = cloudfront.Distribution(
        # #     self,
        # #     "MyDistribution",
        # #     default_behavior=cloudfront.BehaviorOptions(
        # #         origin=cloudfront.S3OriginConfig(
        # #             s3_bucket_source=bucket,
        # #         ),
        # #         cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
        # #         viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        # #     ),
        # #     certificate=cloudfront.Certificate.from_acm_certificate(
        # #         acm_certificate=core.SecretValue.secrets_manager(
        # #             "my/acm/cert", json_field="arn"
        # #         ),
        # #     ),
        # #     domain_names=["example.com", "www.example.com"],
        # # )


        # ##################### CLOUDFRONT #####################

        # distribution = cloudfront.CloudFrontWebDistribution(
        #     self, 
        #     "MyDistribution",
        #     origin_configs=[
        #         cloudfront.SourceConfiguration(
        #             s3_origin_source=cloudfront.S3OriginConfig(
        #                 s3_bucket_source=bucket
        #             ),
        #             behaviors=[
        #                 cloudfront.Behavior(
        #                     is_default_behavior=True,
        #                     default_ttl=Duration.seconds(60),
        #                 )
        #             ],
        #         )
        #     ],
        #     # #TODO try me first
        #     # alias_configuration=cloudfront.AliasConfiguration(
        #     #     names=[fully_qualified_domain_name],
        #     #     acm_cert_ref=certificate.certificate_arn,
        #     #     security_policy=cloudfront.SecurityPolicyProtocol.SSL_V3,  # default
        #     #     ssl_method=cloudfront.SSLMethod.SNI
        #     #     ),
        #     #TODO try me second
        #     viewer_certificate=cloudfront.ViewerCertificate.from_acm_certificate(
        #         certificate=certificate,
        #         aliases=[fully_qualified_domain_name],
        #         security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1_1_2016,  # default
        #         ssl_method=cloudfront.SSLMethod.SNI
        #         )
        # )

        # distribution.node.add_dependency(certificate)
        # distribution.node.add_dependency(deployment)


        # ##################### DNS A RECORD #####################

        # route53.ARecord(
        #     self, 
        #     "AliasRecord",
        #     zone=zone,
        #     record_name=subdomain,
        #     target=route53.RecordTarget.from_alias(
        #         route53_targets.CloudFrontTarget(distribution)
        #     ),
        # )
