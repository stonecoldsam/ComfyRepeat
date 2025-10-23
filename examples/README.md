# ComfyRepeat Examples

This directory contains example scripts and workflows demonstrating ComfyRepeat usage.

## Demo Script

`demo_script.py` - Shows how to use ComfyRepeat programmatically without the GUI.

### Running the Demo

```bash
# Make sure ComfyUI is running
python examples/demo_script.py
```

This will:
1. Connect to ComfyUI
2. Load an example workflow
3. Generate 3 images with different prompts
4. Create a GIF from the frames
5. Export the session as a ZIP

### What You'll Learn

- How to load and configure workflows
- How to submit jobs to ComfyUI
- How to manage sessions and frames
- How to build GIFs programmatically
- How to use ComfyRepeat as a library

## Creating Your Own Scripts

You can use ComfyRepeat modules in your own scripts:

```python
from src.workflow_loader import Workflow
from src.session import Session
from src.comfy_api import ComfyAPI

# Load workflow
workflow = Workflow("path/to/workflow.json")

# Create session
session = Session(output_root="outputs", workflow_name="my_session")

# Connect to ComfyUI
comfy = ComfyAPI("http://127.0.0.1:8188")

# Generate images
workflow.set_positive("your prompt here")
workflow_json = workflow.get_serializable()
prompt_id = comfy.submit_workflow(workflow_json)
result = comfy.poll_until_done(prompt_id)

# Save frame
img_path = result["outputs"][0]["path"]
session.save_frame(img_path, "your prompt", "negative prompt")

# Build GIF
session.build_gif()
```

## More Examples (Coming Soon)

- Batch processing multiple prompts
- Parameter sweep generation
- Style transfer iterations
- Prompt interpolation
- Custom interpolation methods

## Contributing Examples

Have a cool use case? Share it!

1. Create your example script
2. Add documentation
3. Test it thoroughly
4. Submit a PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
