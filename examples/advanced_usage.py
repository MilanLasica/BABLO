"""
Advanced example showing multiple video generations and ownership tracking.
"""

from bablo import VideoStudio


def main():
    """
    Demonstrate advanced features including batch generation and ownership.
    """
    studio = VideoStudio(blockchain_network="ethereum")

    # Generate multiple videos
    prompts = [
        "A futuristic city at night with neon lights",
        "A serene forest with morning mist",
        "A busy marketplace in an ancient city",
    ]

    print("Generating multiple videos...\n")
    videos = []

    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] Generating: {prompt[:50]}...")

        video = studio.generate_video(
            prompt=prompt, duration=15, style="cinematic", resolution="4K"
        )

        # Register each video
        tx_hash = studio.register_video(
            video=video, metadata={"title": f"Generated Video {i}", "sequence": i}
        )

        videos.append({"video": video, "tx_hash": tx_hash})

        print(f"  ✓ Video ID: {video['id']}")
        print(f"  ✓ Tx Hash: {tx_hash}\n")

    # Check ownership of all videos
    print("\nVerifying ownership of all videos:")
    for i, item in enumerate(videos, 1):
        video = item["video"]
        video_hash = studio.storage.compute_hash(video["file_path"])
        owner = studio.get_video_ownership(video_hash)
        print(f"Video {i}: Owner {owner}")

    print("\n✓ All videos generated and registered successfully!")


if __name__ == "__main__":
    main()
