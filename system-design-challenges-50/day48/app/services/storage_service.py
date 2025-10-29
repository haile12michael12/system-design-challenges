from typing import List, Optional, Dict, Any, BinaryIO
from sqlalchemy.orm import Session
import boto3
import json
import logging
from datetime import datetime
import os

from ..config.settings import settings

logger = logging.getLogger(__name__)

class StorageService:
    """Service for managing data lake storage operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self._s3_client = None
    
    @property
    def s3_client(self):
        """Get S3 client (lazy initialization)"""
        if self._s3_client is None:
            self._s3_client = boto3.client(
                's3',
                region_name=settings.storage_region,
                endpoint_url=settings.storage_endpoint
            )
        return self._s3_client
    
    async def upload_file(
        self,
        file_path: str,
        bucket: str = None,
        key: str = None,
        content_type: str = "application/octet-stream"
    ) -> Dict[str, Any]:
        """Upload a file to storage"""
        
        bucket = bucket or settings.storage_bucket
        
        try:
            # Upload file
            self.s3_client.upload_file(
                file_path,
                bucket,
                key,
                ExtraArgs={'ContentType': content_type}
            )
            
            # Get file info
            response = self.s3_client.head_object(Bucket=bucket, Key=key)
            
            result = {
                "success": True,
                "bucket": bucket,
                "key": key,
                "size": response['ContentLength'],
                "etag": response['ETag'],
                "last_modified": response['LastModified']
            }
            
            logger.info(f"Uploaded file: s3://{bucket}/{key}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to upload file {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def upload_data(
        self,
        data: bytes,
        bucket: str = None,
        key: str = None,
        content_type: str = "application/octet-stream"
    ) -> Dict[str, Any]:
        """Upload data directly to storage"""
        
        bucket = bucket or settings.storage_bucket
        
        try:
            # Upload data
            self.s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=data,
                ContentType=content_type
            )
            
            result = {
                "success": True,
                "bucket": bucket,
                "key": key,
                "size": len(data)
            }
            
            logger.info(f"Uploaded data: s3://{bucket}/{key}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to upload data to s3://{bucket}/{key}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def download_file(
        self,
        bucket: str,
        key: str,
        local_path: str = None
    ) -> Dict[str, Any]:
        """Download a file from storage"""
        
        try:
            if local_path:
                # Download to local file
                self.s3_client.download_file(bucket, key, local_path)
                result = {
                    "success": True,
                    "local_path": local_path,
                    "bucket": bucket,
                    "key": key
                }
            else:
                # Download to memory
                response = self.s3_client.get_object(Bucket=bucket, Key=key)
                data = response['Body'].read()
                result = {
                    "success": True,
                    "data": data,
                    "bucket": bucket,
                    "key": key,
                    "size": len(data)
                }
            
            logger.info(f"Downloaded file: s3://{bucket}/{key}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to download file s3://{bucket}/{key}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def list_files(
        self,
        bucket: str = None,
        prefix: str = "",
        max_keys: int = 1000
    ) -> List[Dict[str, Any]]:
        """List files in storage"""
        
        bucket = bucket or settings.storage_bucket
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            files = []
            for obj in response.get('Contents', []):
                files.append({
                    "key": obj['Key'],
                    "size": obj['Size'],
                    "last_modified": obj['LastModified'],
                    "etag": obj['ETag']
                })
            
            logger.info(f"Listed {len(files)} files with prefix: {prefix}")
            return files
            
        except Exception as e:
            logger.error(f"Failed to list files: {str(e)}")
            return []
    
    async def delete_file(
        self,
        bucket: str,
        key: str
    ) -> bool:
        """Delete a file from storage"""
        
        try:
            self.s3_client.delete_object(Bucket=bucket, Key=key)
            logger.info(f"Deleted file: s3://{bucket}/{key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete file s3://{bucket}/{key}: {str(e)}")
            return False
    
    async def delete_files(
        self,
        bucket: str,
        keys: List[str]
    ) -> Dict[str, Any]:
        """Delete multiple files from storage"""
        
        try:
            # Delete up to 1000 objects at once
            objects = [{'Key': key} for key in keys[:1000]]
            
            response = self.s3_client.delete_objects(
                Bucket=bucket,
                Delete={
                    'Objects': objects,
                    'Quiet': False
                }
            )
            
            deleted = len(response.get('Deleted', []))
            errors = len(response.get('Errors', []))
            
            result = {
                "success": True,
                "deleted_count": deleted,
                "error_count": errors,
                "errors": response.get('Errors', [])
            }
            
            logger.info(f"Deleted {deleted} files, {errors} errors")
            return result
            
        except Exception as e:
            logger.error(f"Failed to delete files: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_file_info(
        self,
        bucket: str,
        key: str
    ) -> Optional[Dict[str, Any]]:
        """Get file information"""
        
        try:
            response = self.s3_client.head_object(Bucket=bucket, Key=key)
            
            return {
                "key": key,
                "size": response['ContentLength'],
                "last_modified": response['LastModified'],
                "etag": response['ETag'],
                "content_type": response.get('ContentType'),
                "metadata": response.get('Metadata', {})
            }
            
        except Exception as e:
            logger.error(f"Failed to get file info for s3://{bucket}/{key}: {str(e)}")
            return None
    
    async def generate_presigned_url(
        self,
        bucket: str,
        key: str,
        expiration: int = 3600,
        method: str = "get_object"
    ) -> Optional[str]:
        """Generate a presigned URL for file access"""
        
        try:
            url = self.s3_client.generate_presigned_url(
                method,
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=expiration
            )
            
            logger.info(f"Generated presigned URL for s3://{bucket}/{key}")
            return url
            
        except Exception as e:
            logger.error(f"Failed to generate presigned URL: {str(e)}")
            return None
    
    async def create_partition_structure(
        self,
        table_name: str,
        partition_path: str,
        bucket: str = None
    ) -> bool:
        """Create partition directory structure"""
        
        bucket = bucket or settings.storage_bucket
        key = f"{table_name}/{partition_path}/"
        
        try:
            # Create a marker file to establish the partition
            self.s3_client.put_object(
                Bucket=bucket,
                Key=key + "_SUCCESS",
                Body=b"",
                ContentType="text/plain"
            )
            
            logger.info(f"Created partition structure: s3://{bucket}/{key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create partition structure: {str(e)}")
            return False
