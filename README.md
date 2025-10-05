# Balbo: Desire on Demand

AI-powered video generation platform. Pay with Aeternity tokens to create custom videos from text prompts using the WAN 2.2 5B model via ComfyUI, deployed on Modal.

## Features

- Text-to-video generation using WAN 2.2 5B AI model
- Support for positive and negative prompts
- Real-time progress tracking
- Video preview and download
- Built with React, TypeScript, and Vite
- Serverless deployment with Modal

## Prerequisites

- Node.js (v18 or higher)
- Python 3.8+ (for Modal deployment)
- A ComfyUI instance with WAN 2.2 5B model installed
- Modal account ([sign up at modal.com](https://modal.com))

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Set up Modal

```bash
# Install Modal
pip install modal

# Set up Modal authentication
python3 -m modal setup
```

### 3. Configure ComfyUI Secret

Create a Modal secret with your ComfyUI instance URL:

```bash
modal secret create comfyui-secret COMFYUI_URL=https://your-comfyui-instance.com
```

**Note:** Make sure your ComfyUI instance has the following models installed:
- `wan2.2_ti2v_5B_fp16.safetensors` (main diffusion model)
- `umt5_xxl_fp8_e4m3fn_scaled.safetensors` (CLIP model)
- `wan2.2_vae.safetensors` (VAE model)

### 4. Deploy Modal App

```bash
modal deploy modal_app.py
```

After deployment, Modal will provide you with a URL like:
```
https://yourname--image-animate-workflow-run-workflow.modal.run
```

### 5. Configure Environment Variables

Copy the Modal URL to your `.env` file:

```bash
cp .env.example .env
# Edit .env and add your Modal URL
```

Example `.env`:
```
VITE_WORKFLOW_URL=https://yourname--image-animate-workflow-run-workflow.modal.run
```

### 6. Run the Application

```bash
npm run dev
```

The app will be available at `http://localhost:8080`

## Usage

1. Open the application in your browser
2. Enter a prompt describing what should happen in the video (e.g., "A cat walking on the beach at sunset")
3. Optionally add a negative prompt to specify what to avoid
4. Click "Generate Video"
5. Wait for the video to be generated (this may take a few minutes)
6. View or download your generated video

## Project Structure

```
.
├── src/
│   ├── components/       # React components
│   ├── pages/           # Page components
│   ├── services/        # API service layer
│   └── ...
├── modal_app.py         # Modal deployment configuration
├── n8n_wan_2.2_5b_t2v.json  # Original n8n workflow reference
└── README.md
```

## Workflow Details

The application uses the WAN 2.2 5B text-to-video model with the following configuration:

- **Resolution:** 1280x704
- **Frame count:** 121 frames
- **FPS:** 24
- **Sampler:** uni_pc
- **Steps:** 20
- **CFG Scale:** 5

## Troubleshooting

### Modal deployment fails
- Make sure you've run `python3 -m modal setup`
- Verify your Modal account is active

### ComfyUI connection errors
- Verify your ComfyUI URL is correct in Modal secrets
- Ensure your ComfyUI instance is accessible
- Check that all required models are installed

### Video generation timeout
- The default timeout is 10 minutes
- For complex prompts, generation may take longer
- Check ComfyUI logs for errors

## Development

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## License

MIT
