# ============================================================
# FILE: bedrock_rag.py
# PURPOSE: This file contains ALL the logic for:
#   1. Connecting to Amazon Bedrock
#   2. Sending a question to the Knowledge Base
#   3. Retrieving relevant document chunks (the "R" in RAG)
#   4. Getting the AI to generate a cited answer (the "G" in RAG)
#   5. Uploading documents to S3
#   6. Returning the answer + citations back to the Streamlit UI
# ============================================================


# ============================================================
# SECTION 1: IMPORTS
# ============================================================

import os       
# os = used to read environment variables
# Example: os.getenv("AWS_ACCESS_KEY_ID") reads your key from .env

import logging  
# logging = prints structured messages to the terminal
# Better than print() because it shows timestamps and severity levels

import boto3    
# boto3 = official AWS SDK for Python
# This is how Python talks to AWS services like S3, Bedrock, EC2

from botocore.exceptions import ClientError
# ClientError = the specific error boto3 raises when AWS rejects a request
# Example causes: wrong permissions, wrong region, invalid parameters

from dotenv import load_dotenv
# load_dotenv = reads your .env file and loads the keys as environment variables
# Without this, boto3 cannot find your AWS credentials

from config import (
    AWS_REGION,         # "us-east-1" — which AWS data center to use
    KNOWLEDGE_BASE_ID,  # the ID of your Bedrock Knowledge Base e.g. "ABCD1234EF"
    MODEL_ARN,          # the full ARN path to the Claude AI model
    NUMBER_OF_RESULTS,  # how many document chunks to retrieve per question
    S3_BUCKET_NAME,     # your S3 bucket name e.g. "my-company-knowledgebase-2024"
    S3_PREFIX           # folder inside bucket e.g. "documents/"
)


# ============================================================
# SECTION 2: INITIALIZATION
# Runs once when this file is imported by app.py
# ============================================================

# Load .env file so AWS credentials are available to boto3
# This must happen BEFORE any boto3 calls
load_dotenv()

# Set up the logger for this file
# logging.basicConfig sets the minimum level to show (INFO and above)
# INFO = normal messages, WARNING = something odd, ERROR = something failed
logging.basicConfig(level=logging.INFO)

# Create a logger specifically named "bedrock_rag"
# So terminal messages look like: INFO:bedrock_rag:your message here
logger = logging.getLogger(__name__)
# __name__ automatically becomes "bedrock_rag" (the filename without .py)


# ============================================================
# FUNCTION 1: get_bedrock_client()
# Creates a connection to Amazon Bedrock
# ============================================================

def get_bedrock_client():
    """
    Creates and returns a boto3 client for Amazon Bedrock Agent Runtime.

    WHY "bedrock-agent-runtime"?
    ─────────────────────────────
    AWS Bedrock has two separate services:
      • "bedrock"               → for listing/configuring models (not needed here)
      • "bedrock-agent-runtime" → for RUNNING queries using Knowledge Bases ✅

    HOW AUTHENTICATION WORKS:
    ─────────────────────────────
    boto3 automatically looks for credentials in this order:
      1. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
         ← load_dotenv() above loads these from your .env file
      2. ~/.aws/credentials file (if you ran "aws configure")
      3. IAM Role attached to EC2 (used when deployed on AWS)

    Returns:
        boto3 client object ready to make Bedrock API calls
    """
    try:
        # boto3.client() creates a connection to the specified AWS service
        client = boto3.client(
            service_name="bedrock-agent-runtime",  # which AWS service to connect to
            region_name=AWS_REGION                  # which region e.g. "us-east-1"
        )
        logger.info("Bedrock client created successfully")
        return client

    except Exception as e:
        # If connection fails, log the error and stop execution
        logger.error(f"Failed to create Bedrock client: {e}")
        raise   # "raise" re-throws the error so the caller knows it failed


# ============================================================
# FUNCTION 2: query_knowledge_base()
# The MAIN function — takes a question, returns an AI answer
# ============================================================

def query_knowledge_base(question: str) -> dict:
    """
    This is the core RAG function. It:
      1. Takes the user's question as plain text
      2. Sends it to Amazon Bedrock Knowledge Base
      3. Bedrock converts the question into a vector (embedding)
      4. Bedrock searches the vector database for similar document chunks
      5. The matching chunks are sent to Claude AI as context
      6. Claude generates a grounded answer based ONLY on your documents
      7. We extract the answer + citations and return them

    Args:
        question (str): User's natural language question
                        e.g. "What is the leave policy for new employees?"

    Returns:
        dict: {
            "success":   True or False,
            "answer":    "According to the HR handbook...",
            "citations": [
                {"source": "s3://bucket/docs/file.pdf", "excerpt": "..."},
                ...
            ]
        }
    """

    # Step 1: Get the Bedrock connection
    client = get_bedrock_client()

    try:
        logger.info(f"Querying Knowledge Base with: {question}")

        # Step 2: Call retrieve_and_generate()
        # ─────────────────────────────────────
        # This single API call does BOTH:
        #   RETRIEVE → searches your vector DB for relevant document chunks
        #   GENERATE → sends those chunks + question to Claude to write an answer
        #
        # Parameters explained:
        #   input.text                    = the user's question
        #   type = "KNOWLEDGE_BASE"       = tells Bedrock to use a KB (not direct model)
        #   knowledgeBaseId               = which Knowledge Base to search
        #   modelArn                      = which AI model generates the final answer
        #
        # NOTE: "retrievalConfiguration" was REMOVED — it caused an API error
        # because the current Bedrock API version does not support it here.

        response = client.retrieve_and_generate(
            input={
                "text": question     # the user's question goes here
            },
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,   # your KB ID from config.py
                    "modelArn": MODEL_ARN                   # Claude model ARN from config.py
                }
            }
        )

        # Step 3: Extract the generated answer text
        # response is a large nested dictionary returned by AWS
        # The actual answer lives at: response["output"]["text"]
        answer_text = response["output"]["text"]
        logger.info("Answer received from Bedrock successfully")

        # Step 4: Extract citations
        # ─────────────────────────────────────
        # Bedrock tells us WHICH document chunks it used to form the answer
        # This is called "grounding" — the answer is backed by your actual documents
        # response["citations"] is a list of citation objects
        citations = []

        for citation in response.get("citations", []):
            # Each citation can have multiple "retrievedReferences"
            # (multiple chunks from different parts of the document)
            for reference in citation.get("retrievedReferences", []):

                # The S3 file path where the source document lives
                # Example: "s3://my-company-knowledgebase-2024/documents/hr_policy.pdf"
                source_uri = reference["location"]["s3Location"]["uri"]

                # The actual text snippet from the document that was used
                excerpt = reference["content"]["text"]

                # Trim the excerpt to 300 characters for display
                # (full text can be very long)
                excerpt_preview = (
                    excerpt[:300] + "..."
                    if len(excerpt) > 300
                    else excerpt
                )

                citations.append({
                    "source":  source_uri,      # which document file
                    "excerpt": excerpt_preview  # what text was used from it
                })

        # Step 5: Remove duplicate citations
        # (same document might appear multiple times if multiple chunks matched)
        seen_sources   = set()      # set = stores unique values only
        unique_citations = []

        for cite in citations:
            if cite["source"] not in seen_sources:
                seen_sources.add(cite["source"])
                unique_citations.append(cite)

        # Step 6: Return the final result as a clean dictionary
        return {
            "success":   True,
            "answer":    answer_text,
            "citations": unique_citations
        }

    except ClientError as e:
        # ClientError = AWS rejected the request
        # Common causes:
        #   • Wrong Knowledge Base ID in config.py
        #   • IAM user doesn't have BedrockFullAccess permission
        #   • Model access not enabled in Bedrock console
        error_code    = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        logger.error(f"AWS ClientError [{error_code}]: {error_message}")

        return {
            "success":   False,
            "answer":    f"AWS Error: {error_message}",
            "citations": []
        }

    except Exception as e:
        # Any other unexpected Python error
        logger.error(f"Unexpected error: {e}")

        return {
            "success":   False,
            "answer":    f"An unexpected error occurred: {str(e)}",
            "citations": []
        }


# ============================================================
# FUNCTION 3: upload_document_to_s3()
# Uploads a file from local computer to your S3 bucket
# ============================================================

def upload_document_to_s3(file_path: str, file_name: str) -> bool:
    """
    Uploads a local file to the S3 bucket so Bedrock can index it.

    After uploading, you must go to Bedrock console and click "Sync"
    so Bedrock re-reads the new file and adds it to the vector database.

    Args:
        file_path (str): Full local path to the file
                         Example: "C:/Users/You/AppData/Local/Temp/policy.pdf"
        file_name (str): What to name the file inside S3
                         Example: "policy.pdf"

    Returns:
        bool: True if upload was successful, False if it failed
    """

    # Create a separate S3 client (different service from Bedrock)
    # boto3.client("s3") connects to Amazon S3 storage service
    s3_client = boto3.client("s3", region_name=AWS_REGION)

    # Build the S3 key (full path inside the bucket)
    # S3_PREFIX = "documents/" so s3_key = "documents/policy.pdf"
    # This means the file will be stored as:
    # s3://my-company-knowledgebase-2024/documents/policy.pdf
    s3_key = S3_PREFIX + file_name

    try:
        # upload_file() copies a local file to S3
        # Filename = local file path on your computer
        # Bucket   = your S3 bucket name
        # Key      = destination path inside the bucket
        s3_client.upload_file(
            Filename=file_path,
            Bucket=S3_BUCKET_NAME,
            Key=s3_key
        )

        logger.info(f"Successfully uploaded '{file_name}' to s3://{S3_BUCKET_NAME}/{s3_key}")
        return True     # upload succeeded

    except ClientError as e:
        # Common causes of upload failure:
        #   • IAM user doesn't have S3FullAccess permission
        #   • Bucket name is wrong in config.py
        #   • File doesn't exist at file_path
        logger.error(f"Failed to upload '{file_name}' to S3: {e}")
        return False    # upload failed