"""
S3-Compatible Providers Client Library

This module provides a unified interface for accessing S3-compatible storage services
across multiple cloud providers including AWS S3, Wasabi, Backblaze B2, and DigitalOcean Spaces.
"""

import boto3
from botocore.client import Config
from typing import Optional, Dict, Any, List
import os


class S3CompatibleClient:
    """
    A client for interacting with S3-compatible storage services.
    
    This class provides a unified interface for common S3 operations across
    different cloud providers that support the S3 API.
    """
    
    # Provider configurations
    PROVIDERS = {
        'aws': {
            'endpoint_url': None,  # Uses default AWS endpoints
            'region_name': 'us-east-1',
            'signature_version': 's3v4'
        },
        'wasabi': {
            'endpoint_url': 'https://s3.wasabisys.com',
            'region_name': 'us-east-1',
            'signature_version': 's3v4'
        },
        'backblaze': {
            'endpoint_url': 'https://s3.us-west-000.backblazeb2.com',  # Region-specific
            'region_name': 'us-west-000',
            'signature_version': 's3v4'
        },
        'digitalocean': {
            'endpoint_url': 'https://nyc3.digitaloceanspaces.com',  # Region-specific
            'region_name': 'nyc3',
            'signature_version': 's3v4'
        }
    }
    
    def __init__(
        self,
        provider: str,
        access_key: str,
        secret_key: str,
        endpoint_url: Optional[str] = None,
        region_name: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the S3-compatible client.
        
        Args:
            provider: The cloud provider ('aws', 'wasabi', 'backblaze', 'digitalocean')
            access_key: Access key ID for authentication
            secret_key: Secret access key for authentication
            endpoint_url: Optional custom endpoint URL (overrides provider default)
            region_name: Optional custom region name (overrides provider default)
            **kwargs: Additional arguments passed to boto3.client
        
        Raises:
            ValueError: If the provider is not supported
        """
        if provider not in self.PROVIDERS:
            raise ValueError(
                f"Unsupported provider: {provider}. "
                f"Supported providers: {', '.join(self.PROVIDERS.keys())}"
            )
        
        self.provider = provider
        config_dict = self.PROVIDERS[provider].copy()
        
        # Override with custom values if provided
        if endpoint_url:
            config_dict['endpoint_url'] = endpoint_url
        if region_name:
            config_dict['region_name'] = region_name
        
        # Store region for later use
        self.region_name = config_dict['region_name']
        
        # Create boto3 configuration
        boto_config = Config(signature_version=config_dict['signature_version'])
        
        # Initialize S3 client
        self.client = boto3.client(
            's3',
            endpoint_url=config_dict['endpoint_url'],
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=config_dict['region_name'],
            config=boto_config,
            **kwargs
        )
    
    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List all buckets.
        
        Returns:
            List of bucket information dictionaries
        """
        response = self.client.list_buckets()
        return response.get('Buckets', [])
    
    def create_bucket(self, bucket_name: str) -> Dict[str, Any]:
        """
        Create a new bucket.
        
        Args:
            bucket_name: Name of the bucket to create
            
        Returns:
            Response dictionary from the create operation
        """
        # For AWS S3, regions other than us-east-1 require CreateBucketConfiguration
        if self.provider == 'aws' and self.region_name != 'us-east-1':
            return self.client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region_name}
            )
        else:
            return self.client.create_bucket(Bucket=bucket_name)
    
    def delete_bucket(self, bucket_name: str) -> Dict[str, Any]:
        """
        Delete a bucket.
        
        Args:
            bucket_name: Name of the bucket to delete
            
        Returns:
            Response dictionary from the delete operation
        """
        return self.client.delete_bucket(Bucket=bucket_name)
    
    def upload_file(
        self,
        file_path: str,
        bucket_name: str,
        object_key: Optional[str] = None
    ) -> None:
        """
        Upload a file to a bucket.
        
        Args:
            file_path: Local path to the file to upload
            bucket_name: Name of the destination bucket
            object_key: Optional key for the object (defaults to filename)
            
        Returns:
            None
        """
        if object_key is None:
            object_key = os.path.basename(file_path)
        
        self.client.upload_file(file_path, bucket_name, object_key)
    
    def download_file(
        self,
        bucket_name: str,
        object_key: str,
        file_path: str
    ) -> None:
        """
        Download a file from a bucket.
        
        Args:
            bucket_name: Name of the source bucket
            object_key: Key of the object to download
            file_path: Local path to save the downloaded file
            
        Returns:
            None
        """
        self.client.download_file(bucket_name, object_key, file_path)
    
    def list_objects(
        self,
        bucket_name: str,
        prefix: str = '',
        max_keys: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        List objects in a bucket.
        
        Args:
            bucket_name: Name of the bucket
            prefix: Optional prefix to filter objects
            max_keys: Maximum number of keys to return
            
        Returns:
            List of object information dictionaries
        """
        response = self.client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            MaxKeys=max_keys
        )
        return response.get('Contents', [])
    
    def delete_object(self, bucket_name: str, object_key: str) -> Dict[str, Any]:
        """
        Delete an object from a bucket.
        
        Args:
            bucket_name: Name of the bucket
            object_key: Key of the object to delete
            
        Returns:
            Response dictionary from the delete operation
        """
        return self.client.delete_object(Bucket=bucket_name, Key=object_key)
    
    def get_object(self, bucket_name: str, object_key: str) -> Dict[str, Any]:
        """
        Get an object from a bucket.
        
        Args:
            bucket_name: Name of the bucket
            object_key: Key of the object to retrieve
            
        Returns:
            Response dictionary containing object data and metadata
        """
        return self.client.get_object(Bucket=bucket_name, Key=object_key)
    
    def put_object(
        self,
        bucket_name: str,
        object_key: str,
        data: bytes
    ) -> Dict[str, Any]:
        """
        Put an object into a bucket.
        
        Args:
            bucket_name: Name of the bucket
            object_key: Key for the object
            data: Binary data to upload
            
        Returns:
            Response dictionary from the put operation
        """
        return self.client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
    
    def generate_presigned_url(
        self,
        bucket_name: str,
        object_key: str,
        expiration: int = 3600,
        http_method: str = 'get_object'
    ) -> str:
        """
        Generate a presigned URL for an object.
        
        Args:
            bucket_name: Name of the bucket
            object_key: Key of the object
            expiration: Time in seconds for the presigned URL to remain valid
            http_method: HTTP method for the presigned URL (default: 'get_object')
            
        Returns:
            Presigned URL as a string
        """
        return self.client.generate_presigned_url(
            http_method,
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )


class S3ProviderFactory:
    """
    Factory class for creating S3-compatible clients for different providers.
    """
    
    @staticmethod
    def create_aws_client(
        access_key: str,
        secret_key: str,
        region_name: str = 'us-east-1',
        **kwargs
    ) -> S3CompatibleClient:
        """
        Create an AWS S3 client.
        
        Args:
            access_key: AWS access key ID
            secret_key: AWS secret access key
            region_name: AWS region name
            **kwargs: Additional arguments
            
        Returns:
            Configured S3CompatibleClient instance
        """
        return S3CompatibleClient(
            provider='aws',
            access_key=access_key,
            secret_key=secret_key,
            region_name=region_name,
            **kwargs
        )
    
    @staticmethod
    def create_wasabi_client(
        access_key: str,
        secret_key: str,
        region_name: str = 'us-east-1',
        **kwargs
    ) -> S3CompatibleClient:
        """
        Create a Wasabi client.
        
        Args:
            access_key: Wasabi access key ID
            secret_key: Wasabi secret access key
            region_name: Wasabi region name
            **kwargs: Additional arguments
            
        Returns:
            Configured S3CompatibleClient instance
        """
        # Wasabi region-specific endpoints
        region_endpoints = {
            'us-east-1': 'https://s3.wasabisys.com',
            'us-east-2': 'https://s3.us-east-2.wasabisys.com',
            'us-west-1': 'https://s3.us-west-1.wasabisys.com',
            'eu-central-1': 'https://s3.eu-central-1.wasabisys.com',
            'ap-northeast-1': 'https://s3.ap-northeast-1.wasabisys.com',
        }
        
        endpoint_url = kwargs.pop('endpoint_url', region_endpoints.get(region_name, region_endpoints['us-east-1']))
        
        return S3CompatibleClient(
            provider='wasabi',
            access_key=access_key,
            secret_key=secret_key,
            endpoint_url=endpoint_url,
            region_name=region_name,
            **kwargs
        )
    
    @staticmethod
    def create_backblaze_client(
        access_key: str,
        secret_key: str,
        region_name: str = 'us-west-000',
        **kwargs
    ) -> S3CompatibleClient:
        """
        Create a Backblaze B2 client.
        
        Args:
            access_key: Backblaze application key ID
            secret_key: Backblaze application key
            region_name: Backblaze region name
            **kwargs: Additional arguments
            
        Returns:
            Configured S3CompatibleClient instance
        """
        # Backblaze region-specific endpoints
        endpoint_url = kwargs.pop('endpoint_url', f'https://s3.{region_name}.backblazeb2.com')
        
        return S3CompatibleClient(
            provider='backblaze',
            access_key=access_key,
            secret_key=secret_key,
            endpoint_url=endpoint_url,
            region_name=region_name,
            **kwargs
        )
    
    @staticmethod
    def create_digitalocean_client(
        access_key: str,
        secret_key: str,
        region_name: str = 'nyc3',
        **kwargs
    ) -> S3CompatibleClient:
        """
        Create a DigitalOcean Spaces client.
        
        Args:
            access_key: DigitalOcean Spaces access key
            secret_key: DigitalOcean Spaces secret key
            region_name: DigitalOcean region name (e.g., 'nyc3', 'sfo2', 'sgp1')
            **kwargs: Additional arguments
            
        Returns:
            Configured S3CompatibleClient instance
        """
        # DigitalOcean Spaces region-specific endpoints
        endpoint_url = kwargs.pop('endpoint_url', f'https://{region_name}.digitaloceanspaces.com')
        
        return S3CompatibleClient(
            provider='digitalocean',
            access_key=access_key,
            secret_key=secret_key,
            endpoint_url=endpoint_url,
            region_name=region_name,
            **kwargs
        )
