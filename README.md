# ComfyRepeat

Interactive GUI controller for ComfyUI that guides iterative image evolution (T2I and I2I), allows prompt edits mid-run, saves all frames, and outputs a GIF. Works with any ComfyUI workflow that exposes prompt strings and/or an image input node.

## Features

- 🎨 **Interactive Iteration**: Generate images iteratively with live prompt editing
- 🔄 **T2I and I2I Support**: Works with text-to-image and image-to-image workflows
- 🎬 **GIF Generation**: Automatically creates animated GIFs from your iteration sessions
- 🖼️ **Frame Management**: Save all intermediate frames with full metadata
- ⏯️ **Pause/Resume**: Pause generation, edit prompts, and resume seamlessly
- 📊 **Session Tracking**: Complete metadata for every frame (prompts, parameters, timestamps)
- 🔍 **Lazy Detection**: Automatically detects positive/negative prompt nodes in workflows
- 💾 **Export Ready**: Export sessions as ZIP files with all frames and metadata

## Installation

### Requirements

- Python 3.10 or higher
- ComfyUI running locally or accessible via network

### Install from source

```bash
git clone https://github.com/stonecoldsam/ComfyRepeat.git
cd ComfyRepeat
pip install -r requirements.txt
```

Or install with pip (editable mode):

```bash
pip install -e .
```

## Quick Start

1. **Start ComfyUI** (default: http://127.0.0.1:8188)

2. **Launch ComfyRepeat**:
   ```bash
   python -m src.main
   ```

3. **Load a workflow**: Click "Browse" or enter the path to your ComfyUI workflow JSON file

4. **Generate**: Click "Generate One" or "Iterate N" to start generating images

5. **Build GIF**: Click "Finish & Build GIF" to create your animation

## Usage

### Command Line Options

```bash
python -m src.main [OPTIONS]

Options:
  --workflow PATH          Path to ComfyUI workflow JSON file
  --comfy-url URL         ComfyUI server URL (default: http://127.0.0.1:8188)
  --output-root DIR       Output directory (default: outputs)
  --share                 Create public Gradio share link
  --interpolate METHOD    GIF interpolation: none, blend, rife (default: none)
  --max-frames N          Maximum frames per session (default: 500)
  --verbose              Enable verbose logging
```

### GUI Interface

The GUI is organized into three main sections:

#### Left Panel - Image Display
- **Main Image**: Shows the current/most recent generated image
- **Thumbnails**: Last 5 outputs (click to select as base for next iteration)

#### Right Panel - Controls
- **Workflow**: Load and manage ComfyUI workflow files
- **Prompts**: Edit positive and negative prompts in real-time
- **Parameters**: Adjust steps, CFG, denoise, and seed
- **Controls**: Generate one image, iterate multiple times, pause/resume
- **Session Info**: View frame count, GIF length, and generation progress

### Workflow Detection

ComfyRepeat uses "lazy-as-fuck" detection to find prompt nodes:

1. **Title-based**: Searches for nodes with "positive" or "negative" in the title
2. **Fallback**: Uses the first two text-bearing nodes in order
3. **Image detection**: Finds LoadImage and similar nodes automatically

**Tip**: Name your prompt nodes with "positive" and "negative" in the title for reliable detection.

### Iteration Workflow

1. Load a workflow file
2. (Optional) For I2I workflows, select a base image by clicking a thumbnail
3. Edit prompts and parameters as desired
4. Click "Generate One" for a single image, or "Iterate N" for multiple
5. While iterating, you can:
   - **Pause**: Stop queuing new jobs (current job completes)
   - Edit prompts while paused
   - **Resume**: Continue with updated prompts
6. Click "Finish & Build GIF" to create the final animation

### Output Structure

Each session creates a folder in `outputs/`:

```
outputs/session_20231023_143022/
├── frame_001.png
├── frame_002.png
├── frame_003.png
├── ...
├── evolution.gif
└── metadata.json
```

The `metadata.json` contains:
- Workflow information
- Per-frame prompts and parameters
- Timestamps
- Generation settings

## GIF Interpolation

ComfyRepeat supports optional frame interpolation:

### Blend Interpolation (Built-in)
Creates smooth crossfade transitions between frames using PIL:

```bash
python -m src.main --interpolate blend
```

### RIFE Interpolation (External)
Uses RIFE for AI-powered frame interpolation. Requires RIFE to be installed separately:

```bash
python -m src.main --interpolate rife
```

Configure RIFE path in `.comfy_repeat_config.json`.

## Configuration

Configuration is stored in `.comfy_repeat_config.json` in the project root:

```json
{
  "last_workflow_path": "path/to/workflow.json",
  "output_root": "outputs",
  "comfy_ui_url": "http://127.0.0.1:8188",
  "auto_max_frames": 500,
  "interpolation_method": "none",
  "gif_delay_ms": 100,
  "default_steps": 20,
  "default_cfg": 7.0,
  "default_denoise": 1.0
}
```

## Sample Workflows

Sample workflow files for common use cases can be found in the `workflows/` directory (to be added).

## Troubleshooting

### ComfyUI Connection Issues
- Ensure ComfyUI is running and accessible
- Check the URL in settings or use `--comfy-url`
- Test connection: visit http://127.0.0.1:8188 in your browser

### Workflow Detection Fails
- Name your prompt nodes with "positive" and "negative" in the title
- Ensure your workflow has CLIPTextEncode or similar text nodes
- Check the logs for detection details

### Output Images Not Found
- Verify ComfyUI output directory is accessible
- Check that generations complete successfully in ComfyUI
- Review the logs for file path information

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
flake8 src/
```

## Project Structure

```
comfy_iter_tool/
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── comfy_api.py         # ComfyUI API wrapper
│   ├── workflow_loader.py   # Workflow loading and detection
│   ├── session.py           # Session management
│   ├── gif_builder.py       # GIF creation
│   ├── config.py            # Configuration
│   ├── gui.py               # Gradio GUI
│   └── utils.py             # Utilities
├── workflows/               # Sample workflows
├── outputs/                 # Session outputs
└── docs/                    # Documentation
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- ComfyUI for the amazing stable diffusion interface
- Gradio for the intuitive GUI framework
- The open source community for tools and inspiration
