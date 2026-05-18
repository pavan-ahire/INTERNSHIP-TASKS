# ============================================================
# FILE: config.py
# PURPOSE: Stores ALL settings/constants in one central place.
#          If you need to change something (like region or model),
#          you only change it HERE — not in 5 different files.
# ============================================================

# --- AWS Region ---
# This is the AWS data center region where your services live.
# us-east-1 = North Virginia (most services available here)
AWS_REGION = "us-east-1"

# --- S3 Bucket Name ---
# S3 = Simple Storage Service (AWS cloud file storage)
# This bucket will hold your company documents (PDFs, text files, etc.)
# IMPORTANT: Bucket names must be globally unique across ALL AWS accounts
S3_BUCKET_NAME = "my-company-knowledgebase-2024"

# --- S3 Folder (Prefix) ---
# Inside your S3 bucket, documents will be stored in this folder
# Think of it like a folder path: my-bucket/documents/file.pdf
S3_PREFIX = "documents/"

# --- Bedrock Knowledge Base ID ---
# After you create a Knowledge Base in AWS Bedrock console,
# it gives you a unique ID (like "ABCD1234EF")
# Paste that ID here
KNOWLEDGE_BASE_ID = "9IFFMLYCWX"

# --- Foundation Model ARN ---
# ARN = Amazon Resource Name (unique identifier for any AWS resource)
# This specifies WHICH AI model generates the final answer
# We are using Claude 3 Sonnet — good balance of speed and intelligence
MODEL_ARN = (
    "arn:aws:bedrock:us-east-1::foundation-model/"
    "amazon.nova-lite-v1:0"
   # "anthropic.claude-3-sonnet-20240229-v1:0"
)

# --- How many document chunks to retrieve ---
# When you ask a question, Bedrock searches your docs and finds
# the top N most relevant text chunks to give the AI as context.
# 5 is a good starting point — more = slower but more context
NUMBER_OF_RESULTS = 5

# --- App display settings ---
APP_TITLE = "Enterprise Knowledge Base Q&A"
APP_ICON  = "📚"    # This shows in the browser tab