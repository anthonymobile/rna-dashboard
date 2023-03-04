#!/usr/bin/env python3
import os
import aws_cdk as cdk
from rna_dashboard.rna_dashboard_stack import RNADashboardStack

##################### CONFIG #####################
from dataclasses import dataclass
@dataclass
class Config:
    subdomain: str
    domain: str
cfg = Config(subdomain="rna", domain="crowdr.org")


app = cdk.App()
RNADashboardStack(
    app, 
    "RNADashboardStack",
    cfg=cfg,
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'), 
        region=os.getenv('CDK_DEFAULT_REGION')
        ),
    )

app.synth()
