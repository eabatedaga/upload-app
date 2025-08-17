import aws_cdk as core
import aws_cdk.assertions as assertions

from upload_app.upload_app_stack import AwsAmplifyUploadAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_amplify_upload_app/aws_amplify_upload_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsAmplifyUploadAppStack(app, "aws-amplify-upload-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
