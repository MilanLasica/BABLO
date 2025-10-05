# BABLO

Blockchain-powered creative studio to generate videos based on Wan 2.5

## Overview

BABLO is a decentralized platform that combines blockchain technology with AI-powered video generation. It leverages the Wan 2.5 model to create high-quality videos while using blockchain for content authentication, ownership tracking, and transparent transaction management.

## Features

- **AI-Powered Video Generation**: Generate videos using the Wan 2.5 model
- **Blockchain Integration**: Track video ownership and transactions on the blockchain
- **Decentralized Storage**: Store video metadata and hashes on-chain
- **Content Authentication**: Verify video authenticity through blockchain records
- **Smart Contract Support**: Automate licensing and royalty distribution

## Installation

```bash
# Clone the repository
git clone https://github.com/MilanLasica/BABLO.git
cd BABLO

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from bablo import VideoStudio

# Initialize the studio
studio = VideoStudio(blockchain_network="ethereum")

# Generate a video
video = studio.generate_video(
    prompt="A beautiful sunset over the ocean",
    duration=10,
    style="cinematic"
)

# Register on blockchain
tx_hash = studio.register_video(video)
print(f"Video registered on blockchain: {tx_hash}")
```

## Configuration

Create a `.env` file with your configuration:

```
BLOCKCHAIN_RPC_URL=https://mainnet.infura.io/v3/YOUR_API_KEY
PRIVATE_KEY=your_private_key
WAN_MODEL_API_KEY=your_wan_api_key
```

## Architecture

- `bablo/`: Core library code
  - `studio.py`: Main video studio implementation
  - `blockchain.py`: Blockchain integration
  - `video_generator.py`: Video generation using Wan 2.5
  - `storage.py`: Decentralized storage management
- `examples/`: Usage examples
- `tests/`: Test suite
- `contracts/`: Smart contracts for blockchain integration

## License

MIT License
