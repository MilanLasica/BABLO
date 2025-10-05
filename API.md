# BABLO API Documentation

## Overview

BABLO provides a simple API for generating videos using AI and registering them on the blockchain.

## Classes

### VideoStudio

Main interface for the BABLO platform.

#### Constructor

```python
VideoStudio(
    blockchain_network: str = "ethereum",
    rpc_url: Optional[str] = None,
    private_key: Optional[str] = None,
    wan_api_key: Optional[str] = None
)
```

**Parameters:**
- `blockchain_network`: Target blockchain network (default: "ethereum")
- `rpc_url`: RPC endpoint URL (default: from environment variable)
- `private_key`: Private key for transactions (default: from environment variable)
- `wan_api_key`: API key for Wan 2.5 model (default: from environment variable)

#### Methods

##### generate_video()

Generate a video using the Wan 2.5 model.

```python
studio.generate_video(
    prompt: str,
    duration: int = 10,
    style: str = "realistic",
    **kwargs
) -> Dict[str, Any]
```

**Parameters:**
- `prompt`: Text description of the video to generate
- `duration`: Video duration in seconds (default: 10)
- `style`: Visual style preset (default: "realistic")
  - Options: "realistic", "cinematic", "animated", "artistic"
- `**kwargs`: Additional parameters (resolution, fps, etc.)

**Returns:**
Dictionary containing:
- `id`: Unique video identifier
- `prompt`: Original prompt
- `duration`: Video duration
- `style`: Applied style
- `file_path`: Path to generated video
- `created_at`: Timestamp
- `metadata`: Additional metadata

**Example:**
```python
video = studio.generate_video(
    prompt="A beautiful sunset over the ocean",
    duration=15,
    style="cinematic",
    resolution="4K"
)
```

##### register_video()

Register a video on the blockchain.

```python
studio.register_video(
    video: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> str
```

**Parameters:**
- `video`: Video data dictionary from generate_video()
- `metadata`: Additional metadata to store on-chain

**Returns:**
- Transaction hash (string)

**Example:**
```python
tx_hash = studio.register_video(
    video=video,
    metadata={
        "title": "Ocean Sunset",
        "creator": "Artist Name",
        "license": "CC-BY-4.0"
    }
)
```

##### verify_video()

Verify video authenticity using blockchain records.

```python
studio.verify_video(video_hash: str) -> Dict[str, Any]
```

**Parameters:**
- `video_hash`: Hash of the video file

**Returns:**
Dictionary containing:
- `verified`: Boolean verification status
- `content_hash`: Video hash
- `owner`: Current owner address
- `timestamp`: Registration timestamp
- `network`: Blockchain network

##### get_video_ownership()

Get the current owner of a video.

```python
studio.get_video_ownership(video_hash: str) -> str
```

**Parameters:**
- `video_hash`: Hash of the video file

**Returns:**
- Blockchain address of the current owner

### VideoGenerator

Low-level video generation interface.

#### Methods

##### generate()

```python
generator.generate(
    prompt: str,
    duration: int = 10,
    style: str = "realistic",
    resolution: str = "1080p",
    fps: int = 30,
    **kwargs
) -> Dict[str, Any]
```

### BlockchainManager

Blockchain integration manager.

#### Methods

##### register_content()

```python
blockchain.register_content(
    content_hash: str,
    metadata: Dict[str, Any],
    content_type: str = "video"
) -> str
```

##### verify_content()

```python
blockchain.verify_content(content_hash: str) -> Dict[str, Any]
```

##### transfer_ownership()

```python
blockchain.transfer_ownership(
    content_hash: str,
    new_owner: str
) -> str
```

### StorageManager

Video storage and metadata management.

#### Methods

##### store_metadata()

```python
storage.store_metadata(video_data: Dict[str, Any]) -> str
```

##### load_metadata()

```python
storage.load_metadata(video_id: str) -> Optional[Dict[str, Any]]
```

##### compute_hash()

```python
storage.compute_hash(file_path: str) -> str
```

## Environment Variables

Create a `.env` file with the following:

```
BLOCKCHAIN_RPC_URL=https://mainnet.infura.io/v3/YOUR_API_KEY
PRIVATE_KEY=your_private_key_here
WAN_MODEL_API_KEY=your_wan_api_key_here
STORAGE_PATH=./videos
```

## Error Handling

All methods may raise exceptions:
- `ValueError`: Invalid parameters
- `ConnectionError`: Blockchain connection issues
- `RuntimeError`: Generation or registration failures

## Best Practices

1. **Security**: Never commit your `.env` file
2. **Storage**: Monitor disk usage for video files
3. **Gas Fees**: Check blockchain gas prices before registering
4. **Rate Limits**: Respect API rate limits for video generation
5. **Testing**: Use testnet before mainnet deployment
