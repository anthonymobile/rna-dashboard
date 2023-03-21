from constructs import Construct
from aws_cdk import (
    Stack,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,

)

from types import SimpleNamespace

class RNADashboardStack(Stack):
    def __init__(self, 
                 scope: Construct, 
                 construct_id: str, 
                 cfg: SimpleNamespace, 
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        ##################### FARGATE #####################
        # https://github.com/idanlupinsky/python-cdk-ecs-demo

        vpc = ec2.Vpc(
            self, 
            f"{cfg.stack_name}__EcsVpc", 
            max_azs=2, 
            nat_gateways=0
            )
        
        vpc.add_interface_endpoint('EcrDockerEndpoint', service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER)
        vpc.add_interface_endpoint('EcrEndpoint', service=ec2.InterfaceVpcEndpointAwsService.ECR)
        vpc.add_interface_endpoint('CloudWatchLogsEndpoint', service=ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS)
        
        cluster = ecs.Cluster(
            self, 
            f"{cfg.stack_name}__EcsCluster", 
            vpc=vpc
            )
        
        task_definition = ecs.FargateTaskDefinition(
            self, 
            f"{cfg.stack_name}__DemoServiceTask", 
            family=f"{cfg.stack_name}__DemoServiceTask"
            )

        image = ecs.ContainerImage.from_asset("rna_dashboard/containers/www")

        container = task_definition.add_container("app", image=image)

        # container.add_port_mappings(ecs.PortMapping(container_port=8080))        
        container.add_port_mappings(ecs.PortMapping(container_port=5000))

        ecs_patterns.ApplicationLoadBalancedFargateService(
            self, f"{cfg.stack_name}__DemoService",
            cluster=cluster,
            desired_count=2,
            task_definition=task_definition
            )

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


