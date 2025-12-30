# S3-Compatible Providers

A Python library for accessing S3-compatible storage across multiple cloud providers using AWS SDKs (boto3).

## Supported Providers

- **AWS S3** - Standard Amazon S3
- **Wasabi** - Cost-effective S3-compatible storage
- **Backblaze B2** - Backblaze B2 Cloud Storage with S3-compatible API
- **DigitalOcean Spaces** - DigitalOcean's object storage service

## Features

- Unified interface for all S3-compatible providers
- Support for common S3 operations:
  - Bucket management (list, create, delete)
  - Object operations (upload, download, list, delete)
  - Direct data operations (put/get objects)
  - Presigned URL generation
- Easy provider switching with minimal code changes
- Type hints for better IDE support
- Factory pattern for convenient client creation

## Installation

1. Clone this repository:
```bash
git clone https://github.com/rnishtala-sumo/s3-compatible-providers.git
cd s3-compatible-providers
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from s3_providers import S3CompatibleClient

# Initialize client for any provider
client = S3CompatibleClient(
    provider='aws',  # or 'wasabi', 'backblaze', 'digitalocean'
    access_key='your-access-key',
    secret_key='your-secret-key',
    region_name='us-east-1'
)

# List buckets
buckets = client.list_buckets()
for bucket in buckets:
    print(bucket['Name'])

# Upload a file
client.upload_file('local-file.txt', 'my-bucket', 'remote-file.txt')

# List objects in a bucket
objects = client.list_objects('my-bucket')
for obj in objects:
    print(f"{obj['Key']} - {obj['Size']} bytes")

# Download a file
client.download_file('my-bucket', 'remote-file.txt', 'downloaded-file.txt')
```

### Using the Factory Pattern

```python
from s3_providers import S3ProviderFactory

# Create provider-specific clients
aws_client = S3ProviderFactory.create_aws_client(
    access_key='your-aws-key',
    secret_key='your-aws-secret',
    region_name='us-east-1'
)

wasabi_client = S3ProviderFactory.create_wasabi_client(
    access_key='your-wasabi-key',
    secret_key='your-wasabi-secret',
    region_name='us-east-1'
)

backblaze_client = S3ProviderFactory.create_backblaze_client(
    access_key='your-b2-key-id',
    secret_key='your-b2-application-key',
    region_name='us-west-000'
)

digitalocean_client = S3ProviderFactory.create_digitalocean_client(
    access_key='your-do-key',
    secret_key='your-do-secret',
    region_name='nyc3'
)
```

## Provider-Specific Configuration

### AWS S3

```python
client = S3CompatibleClient(
    provider='aws',
    access_key='your-access-key-id',
    secret_key='your-secret-access-key',
    region_name='us-east-1'  # Any AWS region
)
```

**Available regions**: `us-east-1`, `us-west-1`, `us-west-2`, `eu-west-1`, `eu-central-1`, `ap-southeast-1`, etc.

### Wasabi

```python
client = S3CompatibleClient(
    provider='wasabi',
    access_key='your-wasabi-access-key',
    secret_key='your-wasabi-secret-key',
    region_name='us-east-1'  # or us-east-2, us-west-1, eu-central-1, ap-northeast-1
)
```

**Available regions**: 
- `us-east-1` - US East (N. Virginia)
- `us-east-2` - US East (N. Virginia 2)
- `us-west-1` - US West (Oregon)
- `eu-central-1` - Europe (Amsterdam)
- `ap-northeast-1` - Asia Pacific (Tokyo)

### Backblaze B2

```python
client = S3CompatibleClient(
    provider='backblaze',
    access_key='your-application-key-id',
    secret_key='your-application-key',
    region_name='us-west-000'  # Region depends on your bucket location
)
```

**Note**: Use your Backblaze application key ID and application key. The region code depends on where your bucket was created (e.g., `us-west-000`, `us-west-001`, `eu-central-003`).

### DigitalOcean Spaces

```python
client = S3CompatibleClient(
    provider='digitalocean',
    access_key='your-spaces-access-key',
    secret_key='your-spaces-secret-key',
    region_name='nyc3'  # or sfo2, sfo3, sgp1, fra1, ams3
)
```

**Available regions**:
- `nyc3` - New York 3
- `sfo2`, `sfo3` - San Francisco
- `sgp1` - Singapore
- `fra1` - Frankfurt
- `ams3` - Amsterdam

## API Reference

### S3CompatibleClient Methods

#### Bucket Operations

- `list_buckets()` - List all buckets
- `create_bucket(bucket_name)` - Create a new bucket
- `delete_bucket(bucket_name)` - Delete a bucket

#### Object Operations

- `upload_file(file_path, bucket_name, object_key=None)` - Upload a file
- `download_file(bucket_name, object_key, file_path)` - Download a file
- `list_objects(bucket_name, prefix='', max_keys=1000)` - List objects in a bucket
- `delete_object(bucket_name, object_key)` - Delete an object
- `get_object(bucket_name, object_key)` - Get an object and its metadata
- `put_object(bucket_name, object_key, data)` - Upload data directly as an object
- `generate_presigned_url(bucket_name, object_key, expiration=3600, http_method='get_object')` - Generate a presigned URL

## Examples

See `examples.py` for comprehensive usage examples including:
- Connecting to each provider
- Listing buckets
- Uploading and downloading files
- Working with objects directly (put/get)
- Generating presigned URLs

Run examples:
```bash
# Set your credentials as environment variables
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"

# Run the examples
python examples.py
```

## Configuration with Environment Variables

You can use environment variables to store credentials:

```python
import os
from s3_providers import S3CompatibleClient

client = S3CompatibleClient(
    provider='aws',
    access_key=os.getenv('AWS_ACCESS_KEY_ID'),
    secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)
```

## Error Handling

```python
from botocore.exceptions import ClientError

try:
    client.upload_file('file.txt', 'my-bucket', 'file.txt')
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'NoSuchBucket':
        print("Bucket does not exist")
    elif error_code == 'AccessDenied':
        print("Access denied - check your credentials")
    else:
        print(f"Error: {e}")
```

## Requirements

- Python 3.7+
- boto3 >= 1.26.0
- botocore >= 1.29.0
- python-dotenv >= 1.0.0 (optional, for environment variable management)

## Security Best Practices

1. **Never commit credentials** to version control
2. Use environment variables or secure credential management systems
3. Use IAM roles when running on AWS EC2/ECS/Lambda
4. Implement least-privilege access policies
5. Rotate access keys regularly
6. Use presigned URLs for temporary access instead of sharing credentials

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Open an issue on GitHub
- Check provider documentation for provider-specific issues:
  - [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
  - [Wasabi Documentation](https://wasabi-support.zendesk.com/hc/en-us)
  - [Backblaze B2 Documentation](https://www.backblaze.com/b2/docs/)
  - [DigitalOcean Spaces Documentation](https://docs.digitalocean.com/products/spaces/)
