"""
Example usage of the S3-Compatible Providers library.

This script demonstrates how to use the library to interact with different
S3-compatible storage providers.
"""

from s3_providers import S3CompatibleClient, S3ProviderFactory
import os


def example_aws_s3():
    """Example using AWS S3"""
    print("\n=== AWS S3 Example ===")
    
    # Option 1: Direct instantiation
    client = S3CompatibleClient(
        provider='aws',
        access_key=os.getenv('AWS_ACCESS_KEY_ID', 'your-access-key'),
        secret_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'your-secret-key'),
        region_name='us-east-1'
    )
    
    # Option 2: Using factory
    # client = S3ProviderFactory.create_aws_client(
    #     access_key=os.getenv('AWS_ACCESS_KEY_ID', 'your-access-key'),
    #     secret_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'your-secret-key'),
    #     region_name='us-east-1'
    # )
    
    try:
        # List buckets
        buckets = client.list_buckets()
        print(f"Found {len(buckets)} buckets")
        for bucket in buckets:
            print(f"  - {bucket['Name']}")
    except Exception as e:
        print(f"Error: {e}")


def example_wasabi():
    """Example using Wasabi"""
    print("\n=== Wasabi Example ===")
    
    client = S3ProviderFactory.create_wasabi_client(
        access_key=os.getenv('WASABI_ACCESS_KEY', 'your-access-key'),
        secret_key=os.getenv('WASABI_SECRET_KEY', 'your-secret-key'),
        region_name='us-east-1'
    )
    
    try:
        buckets = client.list_buckets()
        print(f"Found {len(buckets)} buckets")
        for bucket in buckets:
            print(f"  - {bucket['Name']}")
    except Exception as e:
        print(f"Error: {e}")


def example_backblaze():
    """Example using Backblaze B2"""
    print("\n=== Backblaze B2 Example ===")
    
    client = S3ProviderFactory.create_backblaze_client(
        access_key=os.getenv('B2_ACCESS_KEY', 'your-application-key-id'),
        secret_key=os.getenv('B2_SECRET_KEY', 'your-application-key'),
        region_name='us-west-000'
    )
    
    try:
        buckets = client.list_buckets()
        print(f"Found {len(buckets)} buckets")
        for bucket in buckets:
            print(f"  - {bucket['Name']}")
    except Exception as e:
        print(f"Error: {e}")


def example_digitalocean():
    """Example using DigitalOcean Spaces"""
    print("\n=== DigitalOcean Spaces Example ===")
    
    client = S3ProviderFactory.create_digitalocean_client(
        access_key=os.getenv('DO_ACCESS_KEY', 'your-access-key'),
        secret_key=os.getenv('DO_SECRET_KEY', 'your-secret-key'),
        region_name='nyc3'
    )
    
    try:
        buckets = client.list_buckets()
        print(f"Found {len(buckets)} Spaces")
        for bucket in buckets:
            print(f"  - {bucket['Name']}")
    except Exception as e:
        print(f"Error: {e}")


def example_common_operations():
    """Example showing common S3 operations"""
    print("\n=== Common Operations Example ===")
    
    # Initialize client (using AWS as example, but works with any provider)
    client = S3CompatibleClient(
        provider='aws',
        access_key=os.getenv('AWS_ACCESS_KEY_ID', 'your-access-key'),
        secret_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'your-secret-key'),
        region_name='us-east-1'
    )
    
    bucket_name = 'example-bucket-name'
    
    try:
        # Create a bucket
        # print(f"Creating bucket: {bucket_name}")
        # client.create_bucket(bucket_name)
        
        # Upload a file
        # print("Uploading file...")
        # client.upload_file('local-file.txt', bucket_name, 'remote-file.txt')
        
        # List objects
        print(f"Listing objects in bucket: {bucket_name}")
        objects = client.list_objects(bucket_name)
        for obj in objects:
            print(f"  - {obj['Key']} ({obj['Size']} bytes)")
        
        # Download a file
        # print("Downloading file...")
        # client.download_file(bucket_name, 'remote-file.txt', 'downloaded-file.txt')
        
        # Generate presigned URL
        # print("Generating presigned URL...")
        # url = client.generate_presigned_url(bucket_name, 'remote-file.txt', expiration=3600)
        # print(f"Presigned URL: {url}")
        
        # Delete an object
        # print("Deleting object...")
        # client.delete_object(bucket_name, 'remote-file.txt')
        
        # Delete bucket
        # print(f"Deleting bucket: {bucket_name}")
        # client.delete_bucket(bucket_name)
        
    except Exception as e:
        print(f"Error: {e}")


def example_put_get_object():
    """Example showing put and get object operations"""
    print("\n=== Put/Get Object Example ===")
    
    client = S3CompatibleClient(
        provider='aws',
        access_key=os.getenv('AWS_ACCESS_KEY_ID', 'your-access-key'),
        secret_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'your-secret-key'),
        region_name='us-east-1'
    )
    
    bucket_name = 'example-bucket-name'
    object_key = 'test-object.txt'
    
    try:
        # Put object (upload data directly)
        print(f"Putting object: {object_key}")
        data = b"Hello, S3-compatible storage!"
        # client.put_object(bucket_name, object_key, data)
        
        # Get object (retrieve data)
        print(f"Getting object: {object_key}")
        # response = client.get_object(bucket_name, object_key)
        # content = response['Body'].read()
        # print(f"Content: {content.decode('utf-8')}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    print("S3-Compatible Providers - Example Usage")
    print("=" * 50)
    print("\nNOTE: This example requires valid credentials in environment variables.")
    print("Set credentials before running:")
    print("  - AWS: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
    print("  - Wasabi: WASABI_ACCESS_KEY, WASABI_SECRET_KEY")
    print("  - Backblaze: B2_ACCESS_KEY, B2_SECRET_KEY")
    print("  - DigitalOcean: DO_ACCESS_KEY, DO_SECRET_KEY")
    
    # Uncomment the examples you want to run:
    # example_aws_s3()
    # example_wasabi()
    # example_backblaze()
    # example_digitalocean()
    # example_common_operations()
    # example_put_get_object()
    
    print("\n" + "=" * 50)
    print("Examples completed. Uncomment function calls to run specific examples.")
