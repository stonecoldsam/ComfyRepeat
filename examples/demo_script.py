#!/usr/bin/env python3
"""
Demo script showing programmatic usage of ComfyRepeat.

This demonstrates how to use ComfyRepeat modules without the GUI.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.workflow_loader import Workflow
from src.session import Session
from src.comfy_api import ComfyAPI
from src.config import Config
from src import utils

# Setup logging
utils.setup_logging()

def main():
    """Run a simple iteration demo."""
    print("ComfyRepeat Demo Script")
    print("=" * 50)
    
    # Load configuration
    config = Config()
    print(f"ComfyUI URL: {config.get_comfy_url()}")
    
    # Initialize API
    comfy = ComfyAPI(base_url=config.get_comfy_url())
    
    # Check connection
    print("Checking ComfyUI connection...")
    if not comfy.check_connection():
        print("ERROR: Cannot connect to ComfyUI!")
        print(f"Make sure ComfyUI is running at {config.get_comfy_url()}")
        return 1
    print("✓ Connected to ComfyUI")
    
    # Load workflow
    workflow_path = "workflows/example_t2i_simple.json"
    if not os.path.exists(workflow_path):
        print(f"ERROR: Workflow not found: {workflow_path}")
        return 1
    
    print(f"\nLoading workflow: {workflow_path}")
    workflow = Workflow(workflow_path)
    
    info = workflow.get_workflow_info()
    print(f"✓ Workflow loaded")
    print(f"  Type: {'I2I' if info['is_i2i'] else 'T2I'}")
    print(f"  Base positive: {info['base_positive'][:50]}...")
    print(f"  Base negative: {info['base_negative'][:50]}...")
    
    # Create session
    session = Session(
        output_root=config.get_output_root(),
        workflow_name="demo"
    )
    session.set_workflow_path(workflow_path)
    print(f"\n✓ Session created: {session.folder}")
    
    # Define iteration prompts
    prompts = [
        "a serene mountain lake at sunset, golden hour",
        "a serene mountain lake at night, stars reflected",
        "a serene mountain lake in winter, snow covered",
    ]
    
    print(f"\nGenerating {len(prompts)} iterations...")
    print("-" * 50)
    
    # Iterate
    for i, prompt in enumerate(prompts, 1):
        print(f"\nIteration {i}/{len(prompts)}")
        print(f"Prompt: {prompt[:60]}...")
        
        # Update prompts
        workflow.set_positive(prompt)
        workflow.set_negative("blurry, low quality, distorted")
        
        # Set image input for I2I (after first iteration)
        if workflow.is_i2i() and session.last_image:
            workflow.set_image_input(session.last_image)
        
        # Get workflow JSON
        workflow_json = workflow.get_serializable()
        
        # Submit to ComfyUI
        print("  Submitting to ComfyUI...")
        prompt_id = comfy.submit_workflow(workflow_json)
        print(f"  Prompt ID: {prompt_id}")
        
        # Poll until done
        print("  Waiting for generation...")
        result = comfy.poll_until_done(prompt_id)
        
        # Get output
        if not result["outputs"]:
            print("  ERROR: No outputs!")
            continue
        
        output_info = result["outputs"][0]
        img_path = output_info["path"]
        
        # Handle path
        if not os.path.isabs(img_path):
            possible_paths = [
                img_path,
                os.path.join(os.getcwd(), img_path),
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    img_path = p
                    break
        
        if not os.path.exists(img_path):
            print(f"  ERROR: Output not found: {img_path}")
            continue
        
        # Save frame
        frame_path = session.save_frame(
            img_path,
            prompt,
            "blurry, low quality, distorted",
            steps=20,
            cfg=7.0
        )
        print(f"  ✓ Saved: {os.path.basename(frame_path)}")
    
    # Build GIF
    print("\n" + "=" * 50)
    print("Building GIF...")
    gif_path = session.build_gif(delay_ms=1000)
    print(f"✓ GIF created: {gif_path}")
    
    # Export session
    print("\nExporting session...")
    zip_path = session.export_zip()
    print(f"✓ Exported: {zip_path}")
    
    # Summary
    print("\n" + "=" * 50)
    print("Demo Complete!")
    print(f"Frames generated: {session.frame_count}")
    print(f"Session folder: {session.folder}")
    print(f"GIF: {gif_path}")
    print(f"ZIP: {zip_path}")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
