from aws_cdk import (
    Stack,
    Duration,
    aws_apigateway as apigateway,
    CfnOutput,
    aws_lambda_python_alpha as lambda_alpha_,
    aws_lambda as _lambda,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets
)

from constructs import Construct

#TODO: import config somehow
from dataclasses import dataclass

@dataclass
class Config:
    subdomain: str
    domain: str

cfg=Config( subdomain="rna", domain="crowdr.org" )


class RNADashboardStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #FIXME: might need to buld some layers to make this work
        # https://dev.to/aws-builders/build-aws-lambda-layers-with-aws-cdk-4nh5


        # WWW Lambda handler
        my_handler = lambda_alpha_.PythonFunction(
            self, 
            "RNA_Dashboard_WWW_Lambda",
            entry="./rna_dashboard/functions/www/",
            index="app.py",
            handler="handler",
            timeout=Duration.seconds(30) ,
            runtime=_lambda.Runtime.PYTHON_3_8,
            memory_size=2048,
            # provisioned_concurrency_configuration_property=\
            #     lambda_alpha_.CfnAlias.ProvisionedConcurrencyConfigurationProperty(
            #         provisioned_concurrent_executions=2
            #     )
            )

        ################################################################################
        # REST API, Custom Domain
        # following https://cloudbytes.dev/aws-academy/cdk-api-gateway-with-custom-domain
        ################################################################################

        root_domain = cfg.domain
        subdomain = cfg.subdomain
        fully_qualified_domain_name = f"{subdomain}.{root_domain}"

        # get the hosted zone
        my_hosted_zone = route53.HostedZone.from_lookup(
            self,
            "BusObservatoryAPI_HostedZone",
            domain_name=root_domain 
            )

        # CREATE AN ACM CERTIFICATE
        my_certificate = acm.Certificate(
            self,
            "RNA_Dashboard_Stack_Certificate",
            domain_name=fully_qualified_domain_name,
            validation=acm.CertificateValidation.from_dns(hosted_zone=my_hosted_zone)
        )

        # EXPORT THE ARN OF THE CERTIFICATE
        self.certificate_arn = my_certificate.certificate_arn

        # create REST API
        my_api = apigateway.LambdaRestApi(
            self,
            "RNA_Dashboard_WWW_ApiGateway",
            handler=my_handler,
            domain_name=apigateway.DomainNameOptions(
                domain_name=fully_qualified_domain_name,
                certificate=my_certificate,
                security_policy=apigateway.SecurityPolicy.TLS_1_2,
                endpoint_type=apigateway.EndpointType.EDGE,
            )
        )

        # create A record
        route53.ARecord(
            self,
            "RNA_Dashboard__WWW_ApiRecord",
            record_name=subdomain,
            zone=my_hosted_zone,
            target=route53.RecordTarget.from_alias(targets.ApiGateway(my_api)),
        )

        # outputs
        CfnOutput(self, 'Hosted Zone', value=my_hosted_zone.zone_name);
        CfnOutput(self, 'API Url', value=my_api.url);