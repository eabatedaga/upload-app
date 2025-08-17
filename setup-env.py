#!/usr/bin/env python3
"""
Script to extract CDK outputs and create environment file for React app
"""
import json
import subprocess
import sys
import os

def get_cdk_outputs():
    """Get CDK stack outputs"""
    try:
        result = subprocess.run([
            'cdk', 'list', '--json'
        ], capture_output=True, text=True, check=True)
        
        stacks = json.loads(result.stdout)
        if not stacks:
            print("No CDK stacks found")
            return None
            
        stack_name = stacks[0]  # Get first stack
        
        # Get stack outputs
        result = subprocess.run([
            'aws', 'cloudformation', 'describe-stacks',
            '--stack-name', stack_name,
            '--query', 'Stacks[0].Outputs',
            '--output', 'json'
        ], capture_output=True, text=True, check=True)
        
        outputs = json.loads(result.stdout)
        return {output['OutputKey']: output['OutputValue'] for output in outputs}
        
    except subprocess.CalledProcessError as e:
        print(f"Error getting CDK outputs: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def create_env_file(outputs):
    """Create .env file from CDK outputs"""
    env_content = f"""# AWS Configuration - Generated from CDK outputs
REACT_APP_REGION={outputs.get('Region', 'us-east-1')}
REACT_APP_USER_POOL_ID={outputs.get('UserPoolId', '')}
REACT_APP_USER_POOL_CLIENT_ID={outputs.get('UserPoolClientId', '')}
REACT_APP_IDENTITY_POOL_ID={outputs.get('IdentityPoolId', '')}
REACT_APP_S3_BUCKET={outputs.get('S3BucketName', 'upload-bucket-dkfkfhg')}
"""
    
    env_file_path = 'file-upload-frontend/.env'
    with open(env_file_path, 'w') as f:
        f.write(env_content)
    
    print(f"Created {env_file_path} with CDK outputs")
    print("Environment variables:")
    for key, value in outputs.items():
        print(f"  {key}: {value}")

def main():
    print("Setting up environment variables from CDK outputs...")
    
    # Check if we're in the right directory
    if not os.path.exists('cdk.json'):
        print("Error: cdk.json not found. Please run this script from the CDK project root.")
        sys.exit(1)
    
    outputs = get_cdk_outputs()
    if not outputs:
        print("Failed to get CDK outputs. Make sure the stack is deployed.")
        sys.exit(1)
    
    create_env_file(outputs)
    print("Environment setup complete!")

if __name__ == '__main__':
    main()

