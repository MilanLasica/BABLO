"""
Main VideoStudio class for BABLO platform.
"""

from typing import Optional, Dict, Any
from .video_generator import VideoGenerator
from .blockchain import BlockchainManager
from .storage import StorageManager


class VideoStudio:
    """
    Main interface for the BABLO video generation studio.

    Combines AI-powered video generation with blockchain technology
    for content authentication and ownership tracking.
    """

    def __init__(
        self,
        blockchain_network: str = "ethereum",
        rpc_url: Optional[str] = None,
        private_key: Optional[str] = None,
        wan_api_key: Optional[str] = None,
    ):
        """
        Initialize the VideoStudio.

        Args:
            blockchain_network: Target blockchain network (ethereum, polygon, etc.)
            rpc_url: RPC endpoint URL for blockchain connection
            private_key: Private key for blockchain transactions
            wan_api_key: API key for Wan 2.5 model access
        """
        self.blockchain = BlockchainManager(
            network=blockchain_network, rpc_url=rpc_url, private_key=private_key
        )
        self.video_generator = VideoGenerator(api_key=wan_api_key)
        self.storage = StorageManager()

    def generate_video(
        self, prompt: str, duration: int = 10, style: str = "realistic", **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a video using the Wan 2.5 model.

        Args:
            prompt: Text description of the video to generate
            duration: Video duration in seconds
            style: Visual style (realistic, cinematic, animated, etc.)
            **kwargs: Additional generation parameters

        Returns:
            Dictionary containing video metadata and file path
        """
        video_data = self.video_generator.generate(
            prompt=prompt, duration=duration, style=style, **kwargs
        )

        # Store video metadata
        self.storage.store_metadata(video_data)

        return video_data

    def register_video(
        self, video: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Register video on the blockchain.

        Args:
            video: Video data dictionary from generate_video()
            metadata: Additional metadata to store on-chain

        Returns:
            Transaction hash of the blockchain registration
        """
        video_hash = self.storage.compute_hash(video["file_path"])

        tx_hash = self.blockchain.register_content(
            content_hash=video_hash, metadata=metadata or {}, content_type="video"
        )

        return tx_hash

    def verify_video(self, video_hash: str) -> Dict[str, Any]:
        """
        Verify video authenticity using blockchain records.

        Args:
            video_hash: Hash of the video file

        Returns:
            Verification result with ownership and timestamp info
        """
        return self.blockchain.verify_content(video_hash)

    def get_video_ownership(self, video_hash: str) -> str:
        """
        Get the current owner of a video.

        Args:
            video_hash: Hash of the video file

        Returns:
            Blockchain address of the current owner
        """
        return self.blockchain.get_owner(video_hash)
