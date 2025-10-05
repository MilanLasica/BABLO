"""
BABLO - Blockchain-powered creative studio for video generation.
"""

from .studio import VideoStudio
from .video_generator import VideoGenerator
from .blockchain import BlockchainManager

__version__ = "0.1.0"
__all__ = ["VideoStudio", "VideoGenerator", "BlockchainManager"]
