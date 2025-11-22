from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import boto3
from google.cloud import storage as gcs_storage


class ObjectStore(ABC):
    """Abstract base class for object storage"""
    
    @abstractmethod
    def upload_file(self, file_id: str, content: bytes, metadata: Optional[Dict[str, str]] = None) -> str:
        """Upload a file to object storage"""
        pass
    
    @abstractmethod
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Download a file from object storage"""
        pass
    
    @abstractmethod
    def delete_file(self, file_id: str) -> bool:
        """Delete a file from object storage"""
        pass
    
    @abstractmethod
    def file_exists(self, file_id: str) -> bool:
        """Check if a file exists in object storage"""
        pass


class S3Store(ObjectStore):
    """AWS S3 storage implementation"""
    
    def __init__(self, bucket_name: str, region: str = "us-east-1"):
        self.bucket_name = bucket_name
        self.region = region
        self.s3_client = boto3.client("s3", region_name=region)
    
    def upload_file(self, file_id: str, content: bytes, metadata: Optional[Dict[str, str]] = None) -> str:
        """Upload a file to S3"""
        try:
            extra_args = {}
            if metadata:
                extra_args["Metadata"] = metadata
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_id,
                Body=content,
                **extra_args
            )
            return f"s3://{self.bucket_name}/{file_id}"
        except Exception as e:
            raise Exception(f"Failed to upload to S3: {e}")
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Download a file from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_id)
            return response["Body"].read()
        except Exception as e:
            print(f"Error downloading from S3: {e}")
            return None
    
    def delete_file(self, file_id: str) -> bool:
        """Delete a file from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_id)
            return True
        except Exception as e:
            print(f"Error deleting from S3: {e}")
            return False
    
    def file_exists(self, file_id: str) -> bool:
        """Check if a file exists in S3"""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_id)
            return True
        except:
            return False


class GCSStore(ObjectStore):
    """Google Cloud Storage implementation"""
    
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.client = gcs_storage.Client()
        self.bucket = self.client.bucket(bucket_name)
    
    def upload_file(self, file_id: str, content: bytes, metadata: Optional[Dict[str, str]] = None) -> str:
        """Upload a file to GCS"""
        try:
            blob = self.bucket.blob(file_id)
            if metadata:
                blob.metadata = metadata
            blob.upload_from_string(content)
            return f"gs://{self.bucket_name}/{file_id}"
        except Exception as e:
            raise Exception(f"Failed to upload to GCS: {e}")
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Download a file from GCS"""
        try:
            blob = self.bucket.blob(file_id)
            if not blob.exists():
                return None
            return blob.download_as_bytes()
        except Exception as e:
            print(f"Error downloading from GCS: {e}")
            return None
    
    def delete_file(self, file_id: str) -> bool:
        """Delete a file from GCS"""
        try:
            blob = self.bucket.blob(file_id)
            if blob.exists():
                blob.delete()
                return True
            return False
        except Exception as e:
            print(f"Error deleting from GCS: {e}")
            return False
    
    def file_exists(self, file_id: str) -> bool:
        """Check if a file exists in GCS"""
        try:
            blob = self.bucket.blob(file_id)
            return blob.exists()
        except:
            return False


# Placeholder implementation for when no cloud storage is configured
class PlaceholderStore(ObjectStore):
    """Placeholder storage that simulates object storage"""
    
    def __init__(self):
        self.storage = {}
    
    def upload_file(self, file_id: str, content: bytes, metadata: Optional[Dict[str, str]] = None) -> str:
        """Simulate uploading a file"""
        self.storage[file_id] = {
            "content": content,
            "metadata": metadata or {}
        }
        return f"placeholder://{file_id}"
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Simulate downloading a file"""
        if file_id in self.storage:
            return self.storage[file_id]["content"]
        return None
    
    def delete_file(self, file_id: str) -> bool:
        """Simulate deleting a file"""
        if file_id in self.storage:
            del self.storage[file_id]
            return True
        return False
    
    def file_exists(self, file_id: str) -> bool:
        """Check if a file exists"""
        return file_id in self.storage