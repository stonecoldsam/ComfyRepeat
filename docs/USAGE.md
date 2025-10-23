# ComfyRepeat Usage Guide

## Getting Started

### 1. Prerequisites

Before using ComfyRepeat, ensure you have:
- Python 3.10 or higher installed
- ComfyUI running (default: http://127.0.0.1:8188)
- A ComfyUI workflow JSON file

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/stonecoldsam/ComfyRepeat.git
cd ComfyRepeat

# Install dependencies
pip install -r requirements.txt
```

### 3. Basic Usage

Launch the GUI:
```bash
python -m src.main
```

## Workflow Requirements

For ComfyRepeat to work with your workflow, it needs to identify:
1. **Positive prompt node** - for the positive/main prompt
2. **Negative prompt node** - for the negative prompt
3. **Image input node** (optional) - for I2I workflows

### Recommended Setup

Name your prompt nodes in ComfyUI:
- Include "positive" in the title of your positive prompt node
- Include "negative" in the title of your negative prompt node

Example:
- Node title: "Positive Prompt" ✅
- Node title: "CLIP Text Encode (Positive)" ✅
- Node title: "Main Positive" ✅

### Supported Node Types

**Text/Prompt Nodes:**
- CLIPTextEncode
- CLIPTextEncodeSDXL
- CLIPTextEncodeSDXLRefiner
- PrimitiveNode (with text)

**Image Input Nodes:**
- LoadImage
- LoadImageOutput
- ImageLoader
- ImageScaleToTotalPixels

## Step-by-Step Tutorial

### Creating Your First Iteration Session

1. **Start ComfyUI**
   ```bash
   # In your ComfyUI directory
   python main.py
   ```

2. **Launch ComfyRepeat**
   ```bash
   # In the ComfyRepeat directory
   python -m src.main
   ```

3. **Load a Workflow**
   - Click "Browse" and select your workflow JSON
   - Or enter the path directly
   - Click "Load Workflow"

4. **Verify Detection**
   - Check the "Workflow Info" panel
   - Confirm prompt nodes were detected correctly
   - Review the loaded prompts

5. **Generate First Image**
   - Edit prompts if desired
   - Click "Generate One"
   - Wait for ComfyUI to complete

6. **Iterate**
   - The generated image appears in the main view
   - Edit prompts for the next iteration
   - Click "Generate One" again, or "Iterate N" for multiple

7. **Build GIF**
   - When satisfied with your iterations
   - Click "Finish & Build GIF"
   - Find your GIF in the session folder

## Advanced Features

### Image-to-Image Iteration

For I2I workflows:
1. Load an I2I workflow (with LoadImage node)
2. Generate first image normally
3. Each subsequent generation uses the previous output as input
4. Or click thumbnails to select a specific frame as the base

### Pause and Resume

Perfect for mid-iteration adjustments:
1. Click "Iterate N" to start multiple generations
2. Click "Pause" at any time
3. Edit prompts while paused
4. Click "Resume" to continue with new prompts

Note: The current generation will complete before pausing.

### Parameter Tweaking

Adjust generation parameters:
- **Steps**: Number of sampling steps
- **CFG**: Guidance scale (how closely to follow the prompt)
- **Denoise**: Strength of denoising (0=no change, 1=full denoise)
- **Seed**: Random seed (-1 for random)

### Session Management

Each session creates a folder:
```
outputs/session_20231023_143022/
├── frame_001.png
├── frame_002.png
├── ...
├── evolution.gif
└── metadata.json
```

**Export Session:**
- Click "Export ZIP" to package all files
- Share or backup your session easily

**Session Info:**
- Frame count
- GIF duration
- Output folder location
- Current status

## GIF Interpolation

### None (Default)
Direct frame-to-frame animation:
```bash
python -m src.main
```

### Blend Interpolation
Smooth crossfades between frames:
```bash
python -m src.main --interpolate blend
```

Creates additional frames by blending adjacent frames.

### RIFE Interpolation
AI-powered frame interpolation (requires RIFE):
```bash
python -m src.main --interpolate rife
```

1. Install RIFE separately
2. Configure path in `.comfy_repeat_config.json`
3. RIFE generates smoother, more natural transitions

## Configuration

Edit `.comfy_repeat_config.json` to customize:

```json
{
  "comfy_ui_url": "http://127.0.0.1:8188",
  "output_root": "outputs",
  "auto_max_frames": 500,
  "interpolation_method": "none",
  "gif_delay_ms": 100,
  "default_steps": 20,
  "default_cfg": 7.0,
  "default_denoise": 1.0,
  "poll_interval": 1.0,
  "request_timeout": 300
}
```

## Command Line Options

```bash
# Specify workflow
python -m src.main --workflow path/to/workflow.json

# Use different ComfyUI URL
python -m src.main --comfy-url http://192.168.1.100:8188

# Change output directory
python -m src.main --output-root /path/to/outputs

# Enable interpolation
python -m src.main --interpolate blend

# Set max frames
python -m src.main --max-frames 100

# Enable verbose logging
python -m src.main --verbose

# Create public share link
python -m src.main --share
```

## Tips and Tricks

### Prompt Evolution
Start with a general prompt and refine:
1. Generate initial image
2. Pause and add details to prompt
3. Resume and see the evolution
4. Repeat for gradual refinement

### Style Exploration
Iterate with style variations:
1. Start: "photo of a cat"
2. Add: "oil painting style"
3. Change: "watercolor style"
4. Vary: "cyberpunk style"

### Parameter Sweeps
Explore parameter space:
1. Start with low CFG (5.0)
2. Pause after each generation
3. Increase CFG gradually
4. Create GIF showing the progression

### Thumbnail Selection
Use thumbnails strategically:
1. Generate several variations
2. Click the best one
3. Continue iterating from that point
4. Branch your creative path

## Troubleshooting

### ComfyUI Connection Failed
- Ensure ComfyUI is running
- Check the URL in config or use `--comfy-url`
- Test connection: visit http://127.0.0.1:8188

### Workflow Detection Failed
- Add "positive" and "negative" to node titles
- Ensure nodes have text/prompt content
- Check logs for detection details

### Generations Fail
- Verify workflow works in ComfyUI first
- Check ComfyUI console for errors
- Ensure all required models are loaded

### Output Images Not Found
- Check ComfyUI output directory
- Verify file permissions
- Look in ComfyUI logs for save location

### Slow Generation
- Normal - depends on your hardware
- Check if VRAM is sufficient
- Consider reducing image size or steps

## Best Practices

1. **Test First**: Verify workflow in ComfyUI before using ComfyRepeat
2. **Name Clearly**: Use descriptive titles for prompt nodes
3. **Save Often**: Use "Export ZIP" for important sessions
4. **Start Small**: Begin with few iterations to test
5. **Monitor VRAM**: Watch GPU usage during long sessions
6. **Organize Workflows**: Keep workflow files in the `workflows/` folder
7. **Review Metadata**: Check `metadata.json` for detailed information

## Examples

### Simple Text Evolution
```bash
# Load workflow
python -m src.main --workflow workflows/example_t2i_simple.json

# In GUI:
# 1. Start with: "a red apple"
# 2. Generate
# 3. Change to: "a golden apple"
# 4. Generate
# 5. Change to: "a crystal apple"
# 6. Generate
# 7. Build GIF
```

### Image Refinement Loop
```bash
# Load I2I workflow
python -m src.main --workflow workflows/example_i2i_simple.json

# In GUI:
# 1. Generate initial image
# 2. Iterate 10 times with "enhance details"
# 3. Build GIF showing progressive refinement
```

## Getting Help

- Check logs in the GUI for error messages
- Use `--verbose` flag for detailed logging
- Refer to `docs/api-spec.md` for API details
- Report issues on GitHub

## Next Steps

- Explore sample workflows in `workflows/`
- Experiment with interpolation methods
- Create custom workflows in ComfyUI
- Share your creations!
