import os
import re
import boto3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda handler for scraping FIT portal Excel files
    """
    s3_bucket = os.environ.get('S3_BUCKET')
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    
    if not s3_bucket:
        raise ValueError("S3_BUCKET environment variable is required")
    
    s3_client = boto3.client('s3', region_name=aws_region)
    base_url = "https://www.fit-portal.go.jp/PublicInfo"
    
    try:
        # Fetch the main page
        logger.info(f"Fetching HTML from {base_url}")
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()
        
        # Parse HTML and find download links
        soup = BeautifulSoup(response.content, 'html.parser')
        download_links = soup.find_all('a', href=re.compile(r'servlet\.FileDownload\?file='))
        
        logger.info(f"Found {len(download_links)} download links")
        
        processed_files = []
        
        for link in download_links:
            href = link.get('href')
            if not href:
                continue
                
            # Extract file ID from the href
            match = re.search(r'file=([^&]+)', href)
            if not match:
                continue
                
            file_id = match.group(1)
            s3_key = f"raw/{file_id}.xlsx"
            
            # Check if file already exists in S3 (idempotency)
            try:
                s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
                logger.info(f"File {s3_key} already exists in S3, skipping")
                continue
            except s3_client.exceptions.NoSuchKey:
                pass
            
            # Build absolute URL and download file
            absolute_url = urljoin(base_url, href)
            logger.info(f"Downloading file from {absolute_url}")
            
            file_response = requests.get(absolute_url, timeout=60)
            file_response.raise_for_status()
            
            # Save to /tmp directory
            tmp_file_path = f"/tmp/{file_id}.xlsx"
            with open(tmp_file_path, 'wb') as f:
                f.write(file_response.content)
            
            # Upload to S3
            logger.info(f"Uploading {tmp_file_path} to s3://{s3_bucket}/{s3_key}")
            s3_client.upload_file(tmp_file_path, s3_bucket, s3_key)
            
            # Clean up temporary file
            os.remove(tmp_file_path)
            
            processed_files.append({
                'file_id': file_id,
                's3_key': s3_key,
                'source_url': absolute_url
            })
        
        return {
            'statusCode': 200,
            'body': {
                'message': f'Successfully processed {len(processed_files)} files',
                'processed_files': processed_files
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing FIT portal: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e)
            }
        }