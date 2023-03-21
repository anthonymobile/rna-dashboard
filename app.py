#!/usr/bin/env python3
import os, json
import aws_cdk as cdk
from rna_dashboard.rna_dashboard_stack import RNADashboardStack
from types import SimpleNamespace

##################### CONFIG #####################
with open('config/config.json', 'r') as f:
    cfg_data = f.read()
cfg = SimpleNamespace(**json.loads(cfg_data))
cfg.stack_name = f"{cfg.subdomain}-dashboard-stack"
cfg.bucket_name = f"{cfg.subdomain}-dashboard-data"
cfg.region=os.getenv('CDK_DEFAULT_REGION')
print(cfg)

##################### APP #####################
app = cdk.App()
RNADashboardStack(
    app, 
    cfg.stack_name,
    cfg=cfg,
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'), 
        region=os.getenv('CDK_DEFAULT_REGION')
        ),
    )



app.synth()
