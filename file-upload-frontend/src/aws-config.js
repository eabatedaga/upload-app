// AWS Amplify Configuration
// This file contains the configuration for AWS services
// Values will be populated from environment variables or CDK outputs

export const awsConfig = {
  Auth: {
    Cognito: {
      userPoolId: process.env.REACT_APP_USER_POOL_ID || 'us-east-1_XXXXXXXXX',
      userPoolClientId: process.env.REACT_APP_USER_POOL_CLIENT_ID || 'xxxxxxxxxxxxxxxxxxxxxxxxxx',
      identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID || 'us-east-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    }
  },
  Storage: {
    S3: {
      bucket: process.env.REACT_APP_S3_BUCKET || 'upload-bucket-dkfkfhg',
      region: process.env.REACT_APP_REGION || 'us-east-1',
    }
  }
}

// Environment configuration helper
export const getEnvConfig = () => {
  const config = {
    userPoolId: process.env.REACT_APP_USER_POOL_ID,
    userPoolClientId: process.env.REACT_APP_USER_POOL_CLIENT_ID,
    identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID,
    s3Bucket: process.env.REACT_APP_S3_BUCKET,
    region: process.env.REACT_APP_REGION
  }

  // Check if all required environment variables are set
  const missingVars = Object.entries(config)
    .filter(([key, value]) => !value)
    .map(([key]) => key)

  if (missingVars.length > 0) {
    console.warn('Missing environment variables:', missingVars)
    console.warn('Using default values for development. Make sure to set these for production.')
  }

  return config
}

