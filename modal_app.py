"""
Modal app for WAN 2.2 5B text-to-video workflow via ComfyUI
Deploy with: modal deploy modal_app.py
"""

import modal
import os
import json
import time
import random
import asyncio

# Create a Modal app
app = modal.App("image-animate-workflow")

# Define the image with dependencies
image = modal.Image.debian_slim().pip_install(
    "fastapi",
    "httpx",
)

# ComfyUI workflow configuration for WAN 2.2 5B text-to-video
COMFYUI_WORKFLOW_TEMPLATE = {
    "3": {
        "inputs": {
            "seed": None,  # Will be set randomly
            "steps": 20,
            "cfg": 5,
            "sampler_name": "uni_pc",
            "scheduler": "simple",
            "denoise": 1,
            "model": ["48", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["55", 0]
        },
        "class_type": "KSampler",
        "_meta": {"title": "KSampler"}
    },
    "6": {
        "inputs": {
            "text": "${PROMPT}",
            "clip": ["38", 0]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {"title": "CLIP Text Encode (Positive Prompt)"}
    },
    "7": {
        "inputs": {
            "text": "${NEGATIVE_PROMPT}",
            "clip": ["38", 0]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {"title": "CLIP Text Encode (Negative Prompt)"}
    },
    "8": {
        "inputs": {
            "samples": ["3", 0],
            "vae": ["39", 0]
        },
        "class_type": "VAEDecode",
        "_meta": {"title": "VAE Decode"}
    },
    "37": {
        "inputs": {
            "unet_name": "wan2.2_ti2v_5B_fp16.safetensors",
            "weight_dtype": "default"
        },
        "class_type": "UNETLoader",
        "_meta": {"title": "Load Diffusion Model"}
    },
    "38": {
        "inputs": {
            "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
            "type": "wan",
            "device": "default"
        },
        "class_type": "CLIPLoader",
        "_meta": {"title": "Load CLIP"}
    },
    "39": {
        "inputs": {
            "vae_name": "wan2.2_vae.safetensors"
        },
        "class_type": "VAELoader",
        "_meta": {"title": "Load VAE"}
    },
    "48": {
        "inputs": {
            "shift": 8,
            "model": ["37", 0]
        },
        "class_type": "ModelSamplingSD3",
        "_meta": {"title": "ModelSamplingSD3"}
    },
    "55": {
        "inputs": {
            "width": 1280,
            "height": 704,
            "length": 121,
            "batch_size": 1,
            "vae": ["39", 0]
        },
        "class_type": "Wan22ImageToVideoLatent",
        "_meta": {"title": "Wan22ImageToVideoLatent"}
    },
    "57": {
        "inputs": {
            "fps": 24,
            "images": ["8", 0]
        },
        "class_type": "CreateVideo",
        "_meta": {"title": "Create Video"}
    },
    "58": {
        "inputs": {
            "filename_prefix": "video/ComfyUI",
            "format": "auto",
            "codec": "auto",
            "video-preview": "",
            "video": ["57", 0]
        },
        "class_type": "SaveVideo",
        "_meta": {"title": "Save Video"}
    }
}

DEFAULT_NEGATIVE_PROMPT = "色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走"


@app.function(
    image=image,
    timeout=60,  # 1 minute for mock mode
)
@modal.web_endpoint(method="POST")
async def run_workflow(payload: dict):
    """
    WAN 2.2 5B text-to-video workflow endpoint (MOCK MODE)

    Expected payload:
    {
        "prompt": "A cat walking on the beach",
        "negative_prompt": "optional negative prompt",
        "timestamp": "2025-10-05T12:00:00Z"
    }

    Returns:
    {
        "success": true,
        "imageUrl": "url-to-generated-video",
        "message": "Video generated successfully",
        "data": {...}
    }
    """
    from fastapi import HTTPException
    from fastapi.responses import JSONResponse

    try:
        # Get prompts from payload
        prompt = payload.get("prompt", "")
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")

        negative_prompt = payload.get("negative_prompt", DEFAULT_NEGATIVE_PROMPT)

        print(f"[MOCK MODE] Generating video with prompt: {prompt}")

        # Generate random seed
        seed = random.randint(1, 0xFFFFFFFF - 1)

        # Simulate processing time (3-5 seconds)
        processing_time = random.uniform(3, 5)
        print(f"[MOCK MODE] Simulating {processing_time:.1f}s processing time...")
        await asyncio.sleep(processing_time)

        # Mock video URL - using Envato preview video
        video_url = "https://video-previews.elements.envatousercontent.com/09e7c0f5-b67c-4b51-bff7-c87948c75072/watermarked_preview/watermarked_preview.mp4"

        print(f"[MOCK MODE] Video generation complete! Returning mock video URL")

        return JSONResponse(content={
            "success": True,
            "imageUrl": video_url,
            "videoUrl": video_url,
            "message": "Video generated successfully (MOCK MODE)",
            "data": {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "seed": seed,
                "mock": True,
                "note": "This is a mock video. Replace with real ComfyUI when ready."
            }
        })

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in workflow: {str(e)}")
        import traceback
        traceback.print_exc()

        return JSONResponse(
            content={
                "success": False,
                "error": str(e),
                "message": "Video generation failed"
            },
            status_code=500
        )


# Local development function
@app.local_entrypoint()
def main():
    """
    Local test function
    Run with: modal run modal_app.py
    """
    print("Modal WAN 2.2 5B Text-to-Video app is configured!")
    print("\nSetup steps:")
    print("1. Create a Modal secret named 'comfyui-secret' with your COMFYUI_URL")
    print("   modal secret create comfyui-secret COMFYUI_URL=https://your-comfyui-instance.com")
    print("\n2. Deploy the app:")
    print("   modal deploy modal_app.py")
    print("\n3. Copy the generated URL to your .env file as VITE_WORKFLOW_URL")
