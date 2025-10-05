"""
Tests for VideoStudio class.
"""

from bablo import VideoStudio


def test_video_studio_initialization():
    """Test that VideoStudio can be initialized."""
    studio = VideoStudio(blockchain_network="ethereum")
    assert studio is not None
    assert studio.blockchain is not None
    assert studio.video_generator is not None
    assert studio.storage is not None


def test_generate_video():
    """Test video generation."""
    studio = VideoStudio()

    video = studio.generate_video(prompt="Test video", duration=5, style="realistic")

    assert video is not None
    assert "id" in video
    assert "prompt" in video
    assert video["prompt"] == "Test video"
    assert video["duration"] == 5
    assert video["style"] == "realistic"


def test_register_video():
    """Test video registration on blockchain."""
    studio = VideoStudio()

    video = studio.generate_video(prompt="Test video for registration", duration=5)

    tx_hash = studio.register_video(video)

    assert tx_hash is not None
    assert tx_hash.startswith("0x")
    assert len(tx_hash) == 66  # 0x + 64 hex characters


def test_verify_video():
    """Test video verification."""
    studio = VideoStudio()

    video = studio.generate_video(prompt="Test video")
    video_hash = studio.storage.compute_hash(video["file_path"])

    verification = studio.verify_video(video_hash)

    assert verification is not None
    assert "verified" in verification
    assert verification["verified"] is True
    assert "owner" in verification


def test_get_video_ownership():
    """Test getting video ownership."""
    studio = VideoStudio()

    video = studio.generate_video(prompt="Test video")
    video_hash = studio.storage.compute_hash(video["file_path"])

    owner = studio.get_video_ownership(video_hash)

    assert owner is not None
    assert isinstance(owner, str)
    assert len(owner) > 0
