# Quick Start Guide

Get up and running with ComfyRepeat in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/stonecoldsam/ComfyRepeat.git
cd ComfyRepeat

# Install dependencies
pip install -r requirements.txt
```

## Prerequisites

You need ComfyUI running. If you don't have it:

```bash
# In a separate terminal, start ComfyUI
# (Assumes you have ComfyUI installed)
cd /path/to/ComfyUI
python main.py
```

ComfyUI should be accessible at http://127.0.0.1:8188

## First Run

1. **Start ComfyRepeat**
   ```bash
   python -m src.main
   ```

2. **Load a workflow**
   - Click "Browse" button
   - Select a ComfyUI workflow JSON file
   - Or use an example: `workflows/example_t2i_simple.json`
   - Click "Load Workflow"

3. **Generate an image**
   - Review/edit the prompts
   - Click "Generate One"
   - Wait for the image to appear

4. **Iterate**
   - Click "Generate One" again for another iteration
   - Or enter a number and click "Iterate N"

5. **Create your GIF**
   - Click "Finish & Build GIF"
   - Find your GIF in the session folder

## Example Session

Here's a complete example workflow:

```bash
# Start ComfyRepeat
python -m src.main --workflow workflows/example_t2i_simple.json

# In the GUI:
# 1. Edit positive prompt: "a serene mountain lake at sunset"
# 2. Click "Generate One"
# 3. Edit prompt: "a serene mountain lake at night, stars"
# 4. Click "Generate One" 
# 5. Edit prompt: "a serene mountain lake in winter, snow"
# 6. Click "Generate One"
# 7. Click "Finish & Build GIF"
```

You'll get a GIF showing the evolution: sunset → night → winter!

## Command Line Example

```bash
# Specify everything from command line
python -m src.main \
  --workflow workflows/example_t2i_simple.json \
  --output-root my_outputs \
  --interpolate blend \
  --verbose
```

## Next Steps

- Read the full [README.md](README.md)
- Check out [USAGE.md](docs/USAGE.md) for detailed guides
- Explore sample workflows in `workflows/`
- Create your own workflows in ComfyUI

## Common Issues

**"Cannot connect to ComfyUI"**
- Make sure ComfyUI is running at http://127.0.0.1:8188
- Check with: `curl http://127.0.0.1:8188`

**"Could not auto-detect prompt nodes"**
- Add "positive" and "negative" to your node titles in ComfyUI
- Or manually name the nodes in your workflow

**"No outputs from ComfyUI"**
- Verify the workflow works in ComfyUI first
- Check ComfyUI console for errors

## Tips

- 💡 Start with small iteration counts (3-5)
- 💡 Name your prompt nodes clearly in ComfyUI
- 💡 Use "Pause" to edit prompts mid-iteration
- 💡 Click thumbnails to branch from any previous image
- 💡 Export sessions as ZIP for backup/sharing

## Get Help

- Check the [USAGE.md](docs/USAGE.md) guide
- Look at example workflows
- Review logs with `--verbose` flag
- Open an issue on GitHub

Happy iterating! 🎨
