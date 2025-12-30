# S3-Compatible Service Endpoint Formation

This document describes how endpoints are formed for various S3-compatible storage services and how they differ from standard AWS S3.

## AWS S3 (Standard)

### Endpoint Format
AWS S3 uses region-specific endpoints with the bucket name either as a subdomain (virtual-hosted style) or in the path (path-style):

- **Virtual-hosted style**: `https://{bucket-name}.s3.{region}.amazonaws.com`
- **Path-style**: `https://s3.{region}.amazonaws.com/{bucket-name}`
- **Legacy (us-east-1)**: `https://s3.amazonaws.com` (global endpoint)

### Region Examples
- `us-east-1`, `us-west-2`, `eu-west-1`, `ap-southeast-1`, etc.

### Key Characteristics
- Region codes follow AWS standard naming (e.g., `us-east-1`)
- FIPS endpoints available for US regions
- SDK automatically handles bucket location discovery
- Supports both virtual-hosted and path-style URLs

---

## Supported S3-Compatible Services

### 1. Wasabi Hot Cloud Storage

#### Endpoint Format
```
https://s3.{region}.wasabisys.com
```

#### Dynamic Parts
- **{region}**: AWS-compatible region code

#### Region Examples
- `us-east-1` → `https://s3.us-east-1.wasabisys.com`
- `us-east-2` → `https://s3.us-east-2.wasabisys.com`
- `us-west-1` → `https://s3.us-west-1.wasabisys.com`
- `eu-central-1` → `https://s3.eu-central-1.wasabisys.com`
- `ap-northeast-1` → `https://s3.ap-northeast-1.wasabisys.com`

#### Default (No Region)
```
https://s3.wasabisys.com
```

#### Differences from AWS S3
- **Simpler endpoint structure**: No bucket name in subdomain
- **Always path-style access**: Uses `s3.{region}.wasabisys.com/{bucket}` format
- **Different domain**: `.wasabisys.com` instead of `.amazonaws.com`
- **No FIPS endpoints**: Standard endpoints only
- **Signing region**: Set to `us-east-1` by default (can be customized)

---

### 2. Backblaze B2

#### Endpoint Format
```
https://s3.{region}.backblazeb2.com
```

#### Dynamic Parts
- **{region}**: Backblaze-specific region code with numeric suffix

#### Region Examples
- `us-west-004` → `https://s3.us-west-004.backblazeb2.com`
- `us-west-002` → `https://s3.us-west-002.backblazeb2.com`
- `us-east-005` → `https://s3.us-east-005.backblazeb2.com`
- `eu-central-003` → `https://s3.eu-central-003.backblazeb2.com`

#### Default (No Region)
```
https://s3.us-west-004.backblazeb2.com
```

#### Differences from AWS S3
- **Numeric region suffixes**: Uses format like `us-west-004` instead of `us-west-1`
- **Limited regions**: Fewer regions than AWS
- **Path-style only**: Does not support virtual-hosted style URLs
- **Different domain**: `.backblazeb2.com` instead of `.amazonaws.com`
- **Signing region**: Uses `us-west-004` by default
- **No cross-region bucket access**: Each bucket tied to specific region

---

### 3. DigitalOcean Spaces

#### Endpoint Format
```
https://{region}.digitaloceanspaces.com
```

#### Dynamic Parts
- **{region}**: DigitalOcean datacenter code (region comes BEFORE domain)

#### Region Examples
- `nyc3` → `https://nyc3.digitaloceanspaces.com`
- `sfo3` → `https://sfo3.digitaloceanspaces.com`
- `ams3` → `https://ams3.digitaloceanspaces.com`
- `sgp1` → `https://sgp1.digitaloceanspaces.com`
- `fra1` → `https://fra1.digitaloceanspaces.com`
- `blr1` → `https://blr1.digitaloceanspaces.com`

#### Default (No Region)
```
https://nyc3.digitaloceanspaces.com
```

#### Differences from AWS S3
- **Region-first structure**: Region appears at the beginning (`{region}.digitaloceanspaces.com`)
- **No 's3' prefix**: Unlike AWS and others, doesn't use 's3' in the URL
- **Datacenter codes**: Uses datacenter codes (e.g., `nyc3`, `sfo3`) instead of region names
- **Different domain**: `.digitaloceanspaces.com` (unique branding)
- **Path-style access**: Uses `{region}.digitaloceanspaces.com/{bucket}` format
- **Signing region**: Typically uses `us-east-1` for S3 API compatibility
- **CDN integration**: Spaces can be CDN-enabled with separate CDN endpoints

---

### 4. Krutrim Object Storage

#### Endpoint Format
```
https://{location}.kos.olakrutrimsvc.com
```

#### Dynamic Parts
- **{location}**: Data center location code

#### Region
- **Fixed**: `ap-south-1` (India region)

#### Endpoint Examples
- `blr1` (Bangalore) → `https://blr1.kos.olakrutrimsvc.com`
- `hyd1` (Hyderabad) → `https://hyd1.kos.olakrutrimsvc.com`

#### Differences from AWS S3
- **Multiple datacenter endpoints**: Different URLs for different locations within same region
- **Single region**: Only supports `ap-south-1` region
- **Location prefix in URL**: Uses datacenter code (blr1, hyd1) instead of region
- **Path-style only**: Uses `{location}.kos.olakrutrimsvc.com/{bucket}` format
- **Signing region**: Always `ap-south-1`

---

## Key Differences Summary

| Feature | AWS S3 | Wasabi | Backblaze B2 | DigitalOcean | Krutrim |
|---------|--------|--------|--------------|--------------|---------|
| **URL Style** | Virtual-hosted or path | Path-style | Path-style | Path-style | Path-style |
| **Region Format** | `us-east-1` | `us-east-1` | `us-west-004` | `nyc3` | `ap-south-1` |
| **Domain** | `.amazonaws.com` | `.wasabisys.com` | `.backblazeb2.com` | `.digitaloceanspaces.com` | `.olakrutrimsvc.com` |
| **S3 Prefix** | Yes (`s3.`) | Yes (`s3.`) | Yes (`s3.`) | No | No |
| **Auto Region Detection** | Yes | No | No | No | No |
| **FIPS Support** | Yes | No | No | No | No |
| **Signing Region** | Actual region | `us-east-1` | `us-west-004` | `us-east-1` | `ap-south-1` |
| **Endpoint Generation** | Automatic | Automatic | Automatic | Automatic | Fixed |

---

## Implementation Notes

### Path-Style Access
All S3-compatible services use path-style access:
```
https://{endpoint}/{bucket-name}/{object-key}
```

This is configured in the SDK with:
```scala
.withPathStyleAccessEnabled(true)
```
