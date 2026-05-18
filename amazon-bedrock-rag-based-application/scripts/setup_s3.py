import sys
import os

# Fix path so config.py can be found
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

# Load .env file FIRST — before importing boto3 or config
# This reads AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY into environment
from dotenv import load_dotenv
load_dotenv(os.path.join(parent_dir, ".env"))  # explicit path to .env file

# Now import everything else AFTER credentials are loaded
import boto3
from botocore.exceptions import ClientError
from config import AWS_REGION, S3_BUCKET_NAME, S3_PREFIX


def create_s3_bucket():
    """
    Creates an S3 bucket in your AWS account.
    S3 buckets are like folders in the cloud where you store files.
    """
    
    # Create an S3 client (connection to S3 service)
    s3 = boto3.client("s3", region_name=AWS_REGION)
    
    try:
        # For us-east-1, bucket creation is different from other regions
        if AWS_REGION == "us-east-1":
            # us-east-1 does NOT need LocationConstraint
            s3.create_bucket(Bucket=S3_BUCKET_NAME)
        else:
            # All other regions NEED LocationConstraint
            s3.create_bucket(
                Bucket=S3_BUCKET_NAME,
                CreateBucketConfiguration={"LocationConstraint": AWS_REGION}
            )
        
        print(f"Bucket created: {S3_BUCKET_NAME}")
        
        # Block all public access (keep documents private — important!)
        s3.put_public_access_block(
            Bucket=S3_BUCKET_NAME,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": True,         # block public ACLs
                "IgnorePublicAcls": True,         # ignore public ACLs
                "BlockPublicPolicy": True,        # block public bucket policy
                "RestrictPublicBuckets": True     # restrict public bucket access
            }
        )
        print("Public access blocked (documents are private)")
        
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            # Bucket already exists in YOUR account — that's fine
            print(f"Bucket already exists: {S3_BUCKET_NAME}")
        else:
            # Different error — print and stop
            print(f"Error: {e}")
            raise


def upload_sample_documents():
    """
    Uploads all files from the local 'documents/' folder to S3.
    These are the files Bedrock will read and index.
    """
    
    s3 = boto3.client("s3", region_name=AWS_REGION)
    
    # Path to local documents folder
    local_docs_path = "documents"
    
    # os.listdir() returns a list of all files in a folder
    for file_name in os.listdir(local_docs_path):
        
        # Build full local path e.g. "documents/hr_policy.pdf"
        local_file = os.path.join(local_docs_path, file_name)
        
        # S3 key (path inside bucket) e.g. "documents/hr_policy.pdf"
        s3_key = S3_PREFIX + file_name
        
        print(f"Uploading {file_name}...")
        
        # upload_file() copies local file to S3
        s3.upload_file(
            Filename=local_file,       # path on your computer
            Bucket=S3_BUCKET_NAME,     # S3 bucket name
            Key=s3_key                 # path inside the bucket
        )
        
        print(f"Done: s3://{S3_BUCKET_NAME}/{s3_key}")


# ============================================================
# This block runs when you execute this script directly
# i.e. "python scripts/setup_s3.py"
# It does NOT run when this file is imported by another file
# ============================================================
if __name__ == "__main__":
    print("=== S3 Setup Script ===")
    create_s3_bucket()
    upload_sample_documents()
    print("Setup complete! Now create your Bedrock Knowledge Base.")