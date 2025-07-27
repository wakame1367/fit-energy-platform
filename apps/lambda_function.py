import os
import re
import boto3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def extract_filename_from_headers(headers):
    content_disp = headers.get("Content-Disposition")
    if not content_disp:
        return None
    match = re.search(r'filename[*]?=(?:UTF-8\'\')?["\']?([^"\';]+)', content_disp)
    return match.group(1) if match else None

def lambda_handler(event, context):
    s3_bucket = os.environ.get('S3_BUCKET')
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')

    if not s3_bucket:
        raise ValueError("S3_BUCKET environment variable is required")

    s3_client = boto3.client('s3', region_name=aws_region)
    base_url = "https://www.fit-portal.go.jp/PublicInfo"

    try:
        logger.info(f"Fetching HTML from {base_url}")
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        download_links = soup.find_all("a", href=re.compile(r"^/servlet/servlet\.FileDownload"))

        logger.info(f"Found {len(download_links)} download links")
        processed_files = []

        for link in download_links:
            href = link.get('href')
            if not href:
                continue

            match = re.search(r'file=([^&]+)', href)
            if not match:
                continue

            file_id = match.group(1)
            absolute_url = urljoin(base_url, href)

            # First, get filename via HEAD
            logger.info(f"Fetching headers from {absolute_url}")
            head_resp = requests.head(absolute_url, timeout=15)
            head_resp.raise_for_status()
            filename = extract_filename_from_headers(head_resp.headers)
            if not filename:
                filename = f"{file_id}.xlsx"

            s3_key = f"raw/{filename}"

            # Check if file already exists in S3
            try:
                s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
                logger.info(f"File {s3_key} already exists in S3, skipping")
                continue
            except s3_client.exceptions.ClientError as e:
                if e.response['Error']['Code'] != '404':
                    raise

            # Download and upload
            logger.info(f"Downloading file from {absolute_url}")
            file_response = requests.get(absolute_url, timeout=60)
            file_response.raise_for_status()

            tmp_file_path = f"/tmp/{filename}"
            with open(tmp_file_path, 'wb') as f:
                f.write(file_response.content)

            logger.info(f"Uploading {tmp_file_path} to s3://{s3_bucket}/{s3_key}")
            s3_client.upload_file(tmp_file_path, s3_bucket, s3_key)
            os.remove(tmp_file_path)

            processed_files.append({
                'file_id': file_id,
                'filename': filename,
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
