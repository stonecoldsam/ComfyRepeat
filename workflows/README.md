# Sample Workflows

This directory is intended to contain sample ComfyUI workflow JSON files.

## Creating Compatible Workflows

For best results with ComfyRepeat:

1. **Name your prompt nodes**: Include "positive" or "negative" in the node title
2. **Use standard nodes**: CLIPTextEncode, PrimitiveNode, etc.
3. **For I2I workflows**: Include a LoadImage or similar node

## Example Workflow Structure

### T2I (Text-to-Image) Workflow
- Must have at least 2 text/prompt nodes
- First node with "positive" in title = positive prompt
- Second node with "negative" in title = negative prompt

### I2I (Image-to-Image) Workflow
- Same as T2I, plus:
- Must have an image input node (LoadImage, LoadImageOutput, etc.)

## Testing Your Workflow

1. Export your workflow from ComfyUI (Save API Format)
2. Name your prompt nodes appropriately
3. Load it in ComfyRepeat
4. Check the logs to verify detection

## Adding Sample Workflows

To contribute sample workflows:
1. Ensure they work in ComfyUI
2. Name them descriptively (e.g., `sdxl_t2i_basic.json`)
3. Add comments in the filename if needed
4. Test with ComfyRepeat before submitting
