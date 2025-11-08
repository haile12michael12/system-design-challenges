import boto3
from botocore.exceptions import ClientError
import os
from typing import Optional

class S3Storage:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME', 'system-design-coach')

    def upload_diagram(self, file_path: str, object_name: str) -> bool:
        """
        Upload a diagram file to S3
        """
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            return True
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return False

    def download_diagram(self, object_name: str, file_path: str) -> bool:
        """
        Download a diagram file from S3
        """
        try:
            self.s3_client.download_file(self.bucket_name, object_name, file_path)
            return True
        except ClientError as e:
            print(f"Error downloading file from S3: {e}")
            return False

    def get_diagram_url(self, object_name: str) -> Optional[str]:
        """
        Generate a presigned URL for accessing the diagram
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=3600  # 1 hour
            )
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None