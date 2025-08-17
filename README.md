
**This is an experiment, do not use it in production**

# AWS Amplify File Upload Application

A secure file upload application built with AWS CDK (Python), React, AWS Cognito for authentication, and S3 for file storage. Users can authenticate and upload files directly to a specified S3 bucket with automatic overwrite capability.

## Architecture Overview

This application consists of:

- **Frontend**: React application with AWS Amplify UI components
- **Authentication**: AWS Cognito User Pool and Identity Pool
- **Storage**: AWS S3 bucket for file uploads
- **Infrastructure**: AWS CDK with Python for infrastructure as code
- **Deployment**: AWS Amplify for hosting (optional)

## Features

- ✅ Secure user authentication with AWS Cognito
- ✅ Direct file upload to S3 bucket
- ✅ Multiple file selection support
- ✅ Automatic file overwrite capability
- ✅ Responsive web design
- ✅ Real-time upload progress feedback
- ✅ Infrastructure as Code with AWS CDK

## Prerequisites

Before deploying this application, ensure you have:

1. **AWS CLI** installed and configured with appropriate permissions
2. **Node.js** (version 18 or later)
3. **Python** (version 3.8 or later)
4. **AWS CDK** installed globally (`npm install -g aws-cdk`)
5. **AWS Account** with permissions to create:
   - Cognito User Pools and Identity Pools
   - S3 buckets
   - IAM roles and policies
   - Amplify applications (optional)

## Project Structure

```
aws-amplify-upload-app/
├── aws_amplify_upload_app/          # CDK Python package
│   ├── __init__.py
│   └── aws_amplify_upload_app_stack.py  # Main CDK stack
├── file-upload-frontend/            # React frontend application
│   ├── src/
│   │   ├── components/ui/           # UI components (shadcn/ui)
│   │   ├── App.jsx                  # Main React component
│   │   ├── aws-config.js           # AWS configuration
│   │   └── main.jsx                # React entry point
│   ├── .env.example                # Environment variables template
│   └── package.json                # Frontend dependencies
├── app.py                          # CDK app entry point
├── cdk.json                        # CDK configuration
├── setup-env.py                    # Environment setup script
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Deployment Instructions

### Step 1: Clone and Setup the Project

```bash
# If cloning from repository
git clone <repository-url>
cd aws-amplify-upload-app

# Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd file-upload-frontend
npm install  # or pnpm install
cd ..
```

### Step 2: Configure AWS CLI

Ensure your AWS CLI is configured with appropriate credentials:

```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, Region, and Output format
```

### Step 3: Bootstrap CDK (First-time only)

If this is your first time using CDK in your AWS account/region:

```bash
cdk bootstrap
```

### Step 4: Deploy the Infrastructure

Deploy the CDK stack to create all AWS resources:

```bash
# Synthesize the CloudFormation template (optional, for verification)
cdk synth

# Deploy the stack
cdk deploy
```

The deployment will create:
- Cognito User Pool and Identity Pool
- S3 bucket (`upload-bucket-dkfkfhg`)
- IAM roles with appropriate permissions
- Amplify application configuration

### Step 5: Configure Environment Variables

After successful deployment, configure the frontend environment variables:

```bash
# Run the setup script to extract CDK outputs
python3 setup-env.py
```

Alternatively, manually create the `.env` file in the `file-upload-frontend` directory:

```bash
cd file-upload-frontend
cp .env.example .env
# Edit .env with the actual values from CDK outputs
```

The `.env` file should contain:

```env
REACT_APP_REGION=us-east-1
REACT_APP_USER_POOL_ID=us-east-1_XXXXXXXXX
REACT_APP_USER_POOL_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
REACT_APP_IDENTITY_POOL_ID=us-east-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
REACT_APP_S3_BUCKET=upload-bucket-dkfkfhg
```

### Step 6: Test the Application Locally

```bash
cd file-upload-frontend
npm run dev  # or pnpm run dev

# Open http://localhost:5173 in your browser
```

### Step 7: Build and Deploy Frontend (Optional)

For production deployment, build the React application:

```bash
cd file-upload-frontend
npm run build  # or pnpm run build
```

You can then deploy the built files to:
- AWS Amplify Hosting
- AWS S3 with CloudFront
- Any static hosting service

## Usage Instructions

### For End Users

1. **Access the Application**: Navigate to the deployed application URL
2. **Sign Up**: Create a new account using email and password
3. **Verify Email**: Check your email for verification code and complete verification
4. **Sign In**: Log in with your credentials
5. **Upload Files**: 
   - Click "Choose Files" to select one or multiple files
   - Review selected files in the preview area
   - Click "Upload Files" to upload to S3
   - Files with the same name will be automatically overwritten

### For Administrators

Monitor and manage the application through AWS Console:

- **Cognito**: Manage users and authentication settings
- **S3**: View uploaded files and manage bucket settings
- **CloudWatch**: Monitor application logs and metrics
- **IAM**: Review and modify permissions as needed

## Configuration Options

### S3 Bucket Configuration

The S3 bucket is configured with:
- CORS enabled for web uploads
- Private access (no public read)
- Versioning disabled (files are overwritten)

To modify bucket settings, edit `aws_amplify_upload_app_stack.py`:

```python
upload_bucket = s3.Bucket(
    self, "UploadBucket",
    bucket_name="your-custom-bucket-name",
    # Add additional configuration options
)
```

### Cognito Configuration

User Pool settings can be modified in the CDK stack:

```python
user_pool = cognito.UserPool(
    self, "UserPool",
    # Modify authentication requirements
    password_policy=cognito.PasswordPolicy(
        min_length=12,  # Increase minimum password length
        require_symbols=True,  # Require symbols
    ),
    # Add additional configuration
)
```

## Troubleshooting

### Common Issues

1. **CDK Deployment Fails**
   - Ensure AWS CLI is configured correctly
   - Check IAM permissions for CDK operations
   - Verify the S3 bucket name is unique globally

2. **Frontend Build Errors**
   - Ensure all environment variables are set correctly
   - Check Node.js and npm/pnpm versions
   - Clear node_modules and reinstall dependencies

3. **Authentication Issues**
   - Verify Cognito configuration in environment variables
   - Check User Pool and Identity Pool settings
   - Ensure callback URLs are configured correctly

4. **File Upload Failures**
   - Check S3 bucket permissions and CORS configuration
   - Verify IAM roles have appropriate S3 permissions
   - Check browser console for detailed error messages

## Security Considerations

This application implements several security best practices:

1. **Authentication**: All file uploads require user authentication
2. **Authorization**: Users can only access their own files
3. **HTTPS**: All communications are encrypted in transit
4. **IAM Roles**: Least privilege access principles
5. **CORS**: Restricted to specific origins (configure as needed)

## Cost Considerations

This application uses several AWS services that may incur costs:

- **S3**: Storage costs based on uploaded file sizes
- **Cognito**: Free tier includes 50,000 MAUs, then pay per user
- **Data Transfer**: Costs for data transfer out of AWS
- **Amplify**: Hosting costs if using Amplify for frontend

Monitor costs through AWS Cost Explorer and set up billing alerts.

## License

This project is licensed under the MIT License.

---

**Note**: This application is designed for demonstration and development purposes. For production use, consider additional security measures, monitoring, and compliance requirements specific to your use case.
