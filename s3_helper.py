import boto3
from config import Config

def get_s3_client():
    """Create and return an S3 client using credentials from Config."""
    return boto3.client(
        's3',
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_REGION
    )

def upload_file_to_s3(file_obj, bucket_name, object_name=None):
    """Upload a file to an S3 bucket."""
    if not object_name:
        object_name = file_obj.filename
        
    s3_client = get_s3_client()
    s3_client.upload_fileobj(
        file_obj,
        bucket_name,
        object_name
    )
    # Return file URL
    return f"https://{bucket_name}.s3.{Config.AWS_REGION}.amazonaws.com/{object_name}"

def list_files_in_s3(bucket_name):
    """List files in the S3 bucket."""
    s3_client = get_s3_client()
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        return []
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

def delete_file_from_s3(bucket_name, object_name):
    """Delete an object from S3."""
    s3_client = get_s3_client()
    s3_client.delete_object(Bucket=bucket_name, Key=object_name)
