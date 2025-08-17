from aws_cdk import (
    Stack,
    aws_cognito as cognito,
    aws_s3 as s3,
    aws_iam as iam,
    aws_amplify as amplify,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct

class AwsAmplifyUploadAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket for file uploads
        upload_bucket = s3.Bucket(
            self, "UploadBucket",
            bucket_name="upload-bucket-dkfkfhg",
            cors=[
                s3.CorsRule(
                    allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.POST, s3.HttpMethods.PUT, s3.HttpMethods.DELETE],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                    max_age=3000
                )
            ],
            public_read_access=False,
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY  # For demo purposes
        )

        # Create Cognito User Pool
        user_pool = cognito.UserPool(
            self, "UserPool",
            user_pool_name="amplify-upload-user-pool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create User Pool Client
        user_pool_client = cognito.UserPoolClient(
            self, "UserPoolClient",
            user_pool=user_pool,
            user_pool_client_name="amplify-upload-client",
            generate_secret=False,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
                custom=True,
                admin_user_password=True
            ),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=True
                ),
                scopes=[cognito.OAuthScope.OPENID, cognito.OAuthScope.EMAIL, cognito.OAuthScope.PROFILE],
                callback_urls=["http://localhost:3000", "https://localhost:3000"]
            )
        )

        # Create Identity Pool
        identity_pool = cognito.CfnIdentityPool(
            self, "IdentityPool",
            identity_pool_name="amplify_upload_identity_pool",
            allow_unauthenticated_identities=False,
            cognito_identity_providers=[
                cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                    client_id=user_pool_client.user_pool_client_id,
                    provider_name=user_pool.user_pool_provider_name
                )
            ]
        )

        # Create IAM role for authenticated users
        authenticated_role = iam.Role(
            self, "AuthenticatedRole",
            assumed_by=iam.FederatedPrincipal(
                "cognito-identity.amazonaws.com",
                {
                    "StringEquals": {
                        "cognito-identity.amazonaws.com:aud": identity_pool.ref
                    },
                    "ForAnyValue:StringLike": {
                        "cognito-identity.amazonaws.com:amr": "authenticated"
                    }
                },
                "sts:AssumeRoleWithWebIdentity"
            ),
            inline_policies={
                "S3UploadPolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "s3:PutObject",
                                "s3:PutObjectAcl",
                                "s3:GetObject",
                                "s3:DeleteObject"
                            ],
                            resources=[f"{upload_bucket.bucket_arn}/*"]
                        )
                    ]
                )
            }
        )

        # Create IAM role for unauthenticated users (minimal permissions)
        unauthenticated_role = iam.Role(
            self, "UnauthenticatedRole",
            assumed_by=iam.FederatedPrincipal(
                "cognito-identity.amazonaws.com",
                {
                    "StringEquals": {
                        "cognito-identity.amazonaws.com:aud": identity_pool.ref
                    },
                    "ForAnyValue:StringLike": {
                        "cognito-identity.amazonaws.com:amr": "unauthenticated"
                    }
                },
                "sts:AssumeRoleWithWebIdentity"
            )
        )

        # Attach roles to Identity Pool
        cognito.CfnIdentityPoolRoleAttachment(
            self, "IdentityPoolRoleAttachment",
            identity_pool_id=identity_pool.ref,
            roles={
                "authenticated": authenticated_role.role_arn,
                "unauthenticated": unauthenticated_role.role_arn
            }
        )

        # Create Amplify App
        amplify_app = amplify.CfnApp(
            self, "AmplifyApp",
            name="file-upload-app",
            description="AWS Amplify app for file uploads to S3",
            platform="WEB",
            repository="https://github.com/aws-samples/amplify-react-app",  # Placeholder - will be updated
            environment_variables=[
                amplify.CfnApp.EnvironmentVariableProperty(
                    name="REACT_APP_REGION",
                    value=self.region
                ),
                amplify.CfnApp.EnvironmentVariableProperty(
                    name="REACT_APP_USER_POOL_ID",
                    value=user_pool.user_pool_id
                ),
                amplify.CfnApp.EnvironmentVariableProperty(
                    name="REACT_APP_USER_POOL_CLIENT_ID",
                    value=user_pool_client.user_pool_client_id
                ),
                amplify.CfnApp.EnvironmentVariableProperty(
                    name="REACT_APP_IDENTITY_POOL_ID",
                    value=identity_pool.ref
                ),
                amplify.CfnApp.EnvironmentVariableProperty(
                    name="REACT_APP_S3_BUCKET",
                    value=upload_bucket.bucket_name
                )
            ]
        )

        # Output important values
        CfnOutput(
            self, "UserPoolId",
            value=user_pool.user_pool_id,
            description="Cognito User Pool ID"
        )

        CfnOutput(
            self, "UserPoolClientId",
            value=user_pool_client.user_pool_client_id,
            description="Cognito User Pool Client ID"
        )

        CfnOutput(
            self, "IdentityPoolId",
            value=identity_pool.ref,
            description="Cognito Identity Pool ID"
        )

        CfnOutput(
            self, "S3BucketName",
            value=upload_bucket.bucket_name,
            description="S3 Bucket for file uploads"
        )

        CfnOutput(
            self, "AmplifyAppId",
            value=amplify_app.attr_app_id,
            description="Amplify App ID"
        )

        CfnOutput(
            self, "Region",
            value=self.region,
            description="AWS Region"
        )

