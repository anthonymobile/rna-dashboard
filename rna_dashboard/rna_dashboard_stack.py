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

)

from dataclasses import dataclass


class RNADashboardStack(Stack):
    def __init__(self, 
                 scope: Construct, 
                 construct_id: str, 
                 cfg: dataclass, 
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        ##################### WWW HANDLER LAMBDA #####################
        my_handler = lambda_alpha_.PythonFunction(
            self,
            "RNA_Dashboard_WWW_Lambda",
            entry="./rna_dashboard/functions/www/",
            index="app.py",
            handler="handler",
            timeout=Duration.seconds(30),
            runtime=_lambda.Runtime.PYTHON_3_8,
            memory_size=2048,
        )


        ##################### REST API GATEWAY WITH CUSTOM DOMAIN #####################

        root_domain = cfg.domain
        subdomain = cfg.subdomain
        fully_qualified_domain_name = f"{subdomain}.{root_domain}"

        # get the hosted zone
        my_hosted_zone = route53.HostedZone.from_lookup(
            self, "BusObservatoryAPI_HostedZone", domain_name=root_domain
        )

        # create certificate
        my_certificate = acm.Certificate(
            self,
            "RNA_Dashboard_Stack_Certificate",
            domain_name=fully_qualified_domain_name,
            validation=acm.CertificateValidation.from_dns(hosted_zone=my_hosted_zone),
        )

        # export the certificate arn
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
            ),
        )

        # create DNS A record
        route53.ARecord(
            self,
            "RNA_Dashboard__WWW_ApiRecord",
            record_name=subdomain,
            zone=my_hosted_zone,
            target=route53.RecordTarget.from_alias(targets.ApiGateway(my_api)),
        )