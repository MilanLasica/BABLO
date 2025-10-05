"""
Tests for StorageManager class.
"""

import os
import tempfile
import pytest
from bablo.storage import StorageManager


@pytest.fixture
def temp_storage():
    """Create a temporary storage directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_storage_manager_initialization(temp_storage):
    """Test StorageManager initialization."""
    manager = StorageManager(storage_path=temp_storage)
    assert manager is not None
    assert os.path.exists(manager.storage_path)
    assert os.path.exists(manager.metadata_path)


def test_store_metadata(temp_storage):
    """Test storing video metadata."""
    manager = StorageManager(storage_path=temp_storage)

    video_data = {"id": "test_video_123", "prompt": "Test video", "duration": 10}

    metadata_file = manager.store_metadata(video_data)

    assert metadata_file is not None
    assert os.path.exists(metadata_file)


def test_load_metadata(temp_storage):
    """Test loading video metadata."""
    manager = StorageManager(storage_path=temp_storage)

    video_data = {"id": "test_video_456", "prompt": "Test video", "duration": 10}

    manager.store_metadata(video_data)
    loaded_data = manager.load_metadata("test_video_456")

    assert loaded_data is not None
    assert loaded_data["id"] == "test_video_456"
    assert loaded_data["prompt"] == "Test video"


def test_load_nonexistent_metadata(temp_storage):
    """Test loading metadata that doesn't exist."""
    manager = StorageManager(storage_path=temp_storage)

    loaded_data = manager.load_metadata("nonexistent")

    assert loaded_data is None


def test_compute_hash():
    """Test hash computation."""
    manager = StorageManager()

    # Test with non-existent file (should hash the path)
    file_hash = manager.compute_hash("test_file.mp4")

    assert file_hash is not None
    assert len(file_hash) == 64  # SHA-256 produces 64 hex characters


def test_get_storage_info(temp_storage):
    """Test getting storage information."""
    manager = StorageManager(storage_path=temp_storage)

    # Store some test metadata
    manager.store_metadata({"id": "video1"})
    manager.store_metadata({"id": "video2"})

    info = manager.get_storage_info()

    assert info is not None
    assert "video_count" in info
    assert info["video_count"] == 2
    assert "storage_path" in info
