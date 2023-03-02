import aws_cdk as core
import aws_cdk.assertions as assertions

from rna_dashboard.rna_dashboard_stack import RnaDashboardStack

# example tests. To run these tests, uncomment this file along with the example
# resource in rna_dashboard/rna_dashboard_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = RnaDashboardStack(app, "rna-dashboard")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
