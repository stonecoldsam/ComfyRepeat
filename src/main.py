"""
ComfyRepeat - Interactive GUI controller for ComfyUI iterative image evolution.

Main entry point.
"""
import argparse
import logging
import sys
import os

from .config import Config
from .gui import launch_gui
from . import utils

logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ComfyRepeat - Interactive ComfyUI Iteration Tool"
    )
    
    parser.add_argument(
        "--workflow",
        type=str,
        help="Path to ComfyUI workflow JSON file"
    )
    
    parser.add_argument(
        "--comfy-url",
        type=str,
        default="http://127.0.0.1:8188",
        help="ComfyUI server URL (default: http://127.0.0.1:8188)"
    )
    
    parser.add_argument(
        "--output-root",
        type=str,
        default="outputs",
        help="Root directory for output sessions (default: outputs)"
    )
    
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public Gradio share link"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (CLI only, no GUI)"
    )
    
    parser.add_argument(
        "--auto-iterate",
        type=int,
        help="Auto-iterate N times in headless mode"
    )
    
    parser.add_argument(
        "--base-image",
        type=str,
        help="Base image path for I2I workflows"
    )
    
    parser.add_argument(
        "--interpolate",
        choices=["none", "blend", "rife"],
        default="none",
        help="Interpolation method for GIF (default: none)"
    )
    
    parser.add_argument(
        "--max-frames",
        type=int,
        help="Maximum frames per session"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    utils.setup_logging(log_level)
    
    logger.info("ComfyRepeat starting...")
    
    # Load config
    config = Config()
    
    # Apply command line overrides
    if args.comfy_url:
        config.set("comfy_ui_url", args.comfy_url)
    
    if args.output_root:
        config.set("output_root", args.output_root)
    
    if args.workflow:
        config.set_last_workflow(args.workflow)
    
    if args.interpolate:
        config.set("interpolation_method", args.interpolate)
    
    if args.max_frames:
        config.set("auto_max_frames", args.max_frames)
    
    # Run mode
    if args.headless:
        logger.info("Headless mode not yet implemented")
        sys.exit(1)
    else:
        # Launch GUI
        logger.info("Launching GUI...")
        launch_gui(config, share=args.share)


if __name__ == "__main__":
    main()
