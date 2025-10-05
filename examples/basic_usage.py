"""
Basic example of using BABLO to generate and register a video.
"""

import os
from bablo import VideoStudio


def main():
    """
    Demonstrate basic video generation and blockchain registration.
    """
    # Initialize the studio
    print("Initializing BABLO Video Studio...")
    studio = VideoStudio(
        blockchain_network="ethereum",
        rpc_url=os.getenv("BLOCKCHAIN_RPC_URL"),
        private_key=os.getenv("PRIVATE_KEY"),
        wan_api_key=os.getenv("WAN_MODEL_API_KEY"),
    )

    # Generate a video
    print("\nGenerating video from prompt...")
    video = studio.generate_video(
        prompt="A beautiful sunset over the ocean with gentle waves", duration=10, style="cinematic"
    )

    print("\nVideo generated successfully!")
    print(f"Video ID: {video['id']}")
    print(f"File path: {video['file_path']}")
    print(f"Duration: {video['duration']} seconds")
    print(f"Style: {video['style']}")

    # Register the video on blockchain
    print("\nRegistering video on blockchain...")
    tx_hash = studio.register_video(
        video=video,
        metadata={"title": "Ocean Sunset", "creator": "BABLO User", "license": "CC-BY-4.0"},
    )

    print("\nVideo registered on blockchain!")
    print(f"Transaction hash: {tx_hash}")

    # Verify the video
    print("\nVerifying video on blockchain...")
    video_hash = studio.storage.compute_hash(video["file_path"])
    verification = studio.verify_video(video_hash)

    print("\nVerification result:")
    print(f"Verified: {verification['verified']}")
    print(f"Owner: {verification['owner']}")
    print(f"Timestamp: {verification['timestamp']}")


if __name__ == "__main__":
    main()
