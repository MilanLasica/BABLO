"""
Tests for VideoGenerator class.
"""

from bablo.video_generator import VideoGenerator


def test_video_generator_initialization():
    """Test VideoGenerator initialization."""
    generator = VideoGenerator()
    assert generator is not None
    assert generator.model_version == "wan-2.5"


def test_generate_video():
    """Test video generation."""
    generator = VideoGenerator()

    video_data = generator.generate(prompt="A test video", duration=10, style="realistic")

    assert video_data is not None
    assert "id" in video_data
    assert "prompt" in video_data
    assert video_data["prompt"] == "A test video"
    assert video_data["duration"] == 10
    assert video_data["style"] == "realistic"
    assert video_data["model"] == "wan-2.5"


def test_generate_video_with_custom_params():
    """Test video generation with custom parameters."""
    generator = VideoGenerator()

    video_data = generator.generate(
        prompt="Custom video", duration=15, style="cinematic", resolution="4K", fps=60
    )

    assert video_data["resolution"] == "4K"
    assert video_data["fps"] == 60


def test_video_id_generation():
    """Test that video IDs are unique."""
    generator = VideoGenerator()

    video1 = generator.generate(prompt="Video 1")
    video2 = generator.generate(prompt="Video 2")

    assert video1["id"] != video2["id"]


def test_get_generation_status():
    """Test generation status check."""
    generator = VideoGenerator()

    video = generator.generate(prompt="Test")
    status = generator.get_generation_status(video["id"])

    assert status is not None
    assert "status" in status
    assert "progress" in status
