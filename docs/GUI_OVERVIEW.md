# ComfyRepeat GUI Overview

## Interface Layout

The ComfyRepeat GUI is divided into two main columns with controls organized logically.

### Left Column - Image Display

#### Main Image (Large)
- Displays the current/most recent generated image
- Updates after each generation
- Full-size preview of your iteration

#### Recent Outputs Thumbnails (Row of 5)
- Shows the last 5 generated frames
- Click any thumbnail to select it as the base for next iteration
- Useful for branching your creative path
- Thumbnails update automatically after each generation

### Right Column - Controls

#### 1. Workflow Section
```
┌─ Workflow ─────────────────────────┐
│ [Workflow Path Input Field]        │
│ [Load Workflow] [Browse File]      │
│ [Workflow Info Display]            │
└────────────────────────────────────┘
```
- Enter or browse for workflow JSON file
- Shows workflow type (T2I/I2I) and detected nodes
- Auto-saves last used workflow

#### 2. Prompts Section
```
┌─ Prompts ──────────────────────────┐
│ Positive Prompt:                   │
│ ┌─────────────────────────────────┐│
│ │ Your positive prompt text...    ││
│ │ (Multi-line text area)          ││
│ └─────────────────────────────────┘│
│                                    │
│ Negative Prompt:                   │
│ ┌─────────────────────────────────┐│
│ │ Your negative prompt text...    ││
│ └─────────────────────────────────┘│
└────────────────────────────────────┘
```
- Edit prompts in real-time
- Pre-populated from workflow
- Changes apply to next generation
- Can edit while paused

#### 3. Parameters Section
```
┌─ Parameters ───────────────────────┐
│ Steps: [20]    CFG: [7.0]          │
│ Denoise: [===|---] 1.0  Seed: [-1] │
└────────────────────────────────────┘
```
- **Steps**: Sampling steps (quality vs speed)
- **CFG**: Guidance scale (prompt adherence)
- **Denoise**: Strength for I2I (0=no change, 1=full)
- **Seed**: Random seed (-1 for random)

#### 4. Controls Section
```
┌─ Controls ─────────────────────────┐
│ [Generate One] [Iterate N: 5]      │
│ [Iterate N] [Pause] [Resume]       │
│ [Finish & Build GIF] [Export ZIP]  │
└────────────────────────────────────┘
```
- **Generate One**: Create single image
- **Iterate N**: Generate N images in sequence
- **Pause**: Stop queueing (current completes)
- **Resume**: Continue with updated prompts
- **Finish & Build GIF**: Create animation
- **Export ZIP**: Package entire session

#### 5. Session Info Section
```
┌─ Session Info ─────────────────────┐
│ Status: Ready                      │
│ Frames: 5                          │
│ GIF length: 0.5s                   │
│ Folder: outputs/session_...        │
│ Avg gen time: 12.3s                │
└────────────────────────────────────┘
```
- Real-time status updates
- Frame count tracking
- Estimated GIF duration
- Session folder location
- Generation time statistics

#### 6. Additional Controls
```
[Open Output Folder]
```
- Quick access to session folder

#### 7. Logs Section
```
┌─ Logs ─────────────────────────────┐
│ Loaded workflow: example_t2i.json  │
│ Generated frame 1 in 12.3s         │
│ Paused (current will complete)     │
└────────────────────────────────────┘
```
- Shows recent messages
- Errors and warnings
- Generation progress
- File operations

## Typical Workflow

### First Time Setup
1. Click "Browse" under Workflow
2. Select your ComfyUI workflow JSON
3. Click "Load Workflow"
4. Verify prompts loaded correctly

### Generating Images
1. Review/edit prompts
2. Adjust parameters if needed
3. Click "Generate One"
4. Wait for image to appear
5. Image shows in main view + thumbnail row

### Iterating
1. After first image generated
2. Enter number in "Iterate N Times" field
3. Click "Iterate N" button
4. Each iteration uses previous output
5. Watch thumbnails update

### Mid-Iteration Editing
1. While iteration running, click "Pause"
2. Current generation completes
3. Edit prompts as desired
4. Click "Resume" to continue

### Creating GIF
1. When satisfied with frames
2. Click "Finish & Build GIF"
3. GIF saved in session folder
4. Ready to view/share

### Exporting
1. Click "Export ZIP" anytime
2. Gets ZIP of entire session
3. Includes all frames + metadata
4. Ready to backup/share

## Visual States

### Status Indicators
- **Ready**: Green - Ready for generation
- **Generating**: Blue - ComfyUI processing
- **Paused**: Yellow - Waiting for resume
- **Error**: Red - Check logs

### Thumbnail States
- **Empty**: Gray placeholder (no image yet)
- **Normal**: Clickable thumbnail
- **Selected**: Highlighted border (chosen as base)

## Tips for Best Experience

### Layout
- Resize window for comfortable view
- Left side focuses on visual output
- Right side for all controls
- Logs at bottom for monitoring

### Workflow
1. Load workflow first
2. Test with "Generate One"
3. Verify output before iterating
4. Use pause for creative changes
5. Export when satisfied

### Performance
- Status updates in real-time
- Thumbnails load as generated
- Session info refreshes automatically
- Minimal clicking required

## Keyboard Shortcuts

Currently uses default Gradio shortcuts:
- Tab: Navigate between fields
- Enter: Submit in text fields
- Click: Select thumbnails

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Mobile Support

The Gradio interface adapts to mobile:
- Stacked layout on small screens
- Touch-friendly controls
- Swipe between images

## Sharing

Use the `--share` flag to create a public link:
```bash
python -m src.main --share
```
Creates a temporary public URL for sharing with others.

## Customization

Future versions may support:
- Custom themes
- Rearrangeable layouts
- Keyboard shortcuts
- Additional parameter controls
- Real-time previews

## Troubleshooting Display

If images don't appear:
1. Check ComfyUI connection
2. Verify workflow generates output
3. Check logs for errors
4. Ensure output paths accessible

If layout looks wrong:
1. Refresh browser
2. Clear cache
3. Try different browser
4. Check console for errors

## Next Steps

- Try the example workflows
- Experiment with parameters
- Create custom workflows
- Share your creations!

For detailed usage instructions, see [USAGE.md](USAGE.md).
