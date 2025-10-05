"""
Storage management for video files and metadata.
"""

import os
import json
import hashlib
from typing import Dict, Any, Optional


class StorageManager:
    """
    Manages storage of video files and associated metadata.
    """

    def __init__(self, storage_path: str = "./videos"):
        """
        Initialize storage manager.

        Args:
            storage_path: Base path for video storage
        """
        self.storage_path = storage_path
        self.metadata_path = os.path.join(storage_path, "metadata")

        # Create storage directories if they don't exist
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(self.metadata_path, exist_ok=True)

    def store_metadata(self, video_data: Dict[str, Any]) -> str:
        """
        Store video metadata to disk.

        Args:
            video_data: Video metadata dictionary

        Returns:
            Path to metadata file
        """
        video_id = video_data.get("id")
        metadata_file = os.path.join(self.metadata_path, f"{video_id}.json")

        with open(metadata_file, "w") as f:
            json.dump(video_data, f, indent=2)

        return metadata_file

    def load_metadata(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Load video metadata from disk.

        Args:
            video_id: Video identifier

        Returns:
            Video metadata dictionary or None if not found
        """
        metadata_file = os.path.join(self.metadata_path, f"{video_id}.json")

        if not os.path.exists(metadata_file):
            return None

        with open(metadata_file, "r") as f:
            return json.load(f)

    def compute_hash(self, file_path: str) -> str:
        """
        Compute SHA-256 hash of a file.

        Args:
            file_path: Path to the file

        Returns:
            Hexadecimal hash string
        """
        sha256_hash = hashlib.sha256()

        # For files that don't exist yet, return hash of the path
        if not os.path.exists(file_path):
            return hashlib.sha256(file_path.encode("utf-8")).hexdigest()

        # For existing files, compute actual file hash
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get information about storage usage.

        Returns:
            Storage statistics
        """
        video_count = len([f for f in os.listdir(self.metadata_path) if f.endswith(".json")])

        return {
            "storage_path": self.storage_path,
            "video_count": video_count,
            "metadata_path": self.metadata_path,
        }
