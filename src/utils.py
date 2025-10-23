"""
Helper utilities for ComfyRepeat.
"""
import os
import logging
from datetime import datetime
from typing import List
import glob


def setup_logging(level=logging.INFO):
    """Setup logging with a consistent format."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def create_timestamped_folder(base_dir: str = "outputs") -> str:
    """Create a timestamped folder for a session."""
    os.makedirs(base_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join(base_dir, f"session_{timestamp}")
    os.makedirs(folder, exist_ok=True)
    return folder


def get_sorted_frame_files(folder: str, pattern: str = "frame_*.png") -> List[str]:
    """Get sorted list of frame files from a folder."""
    files = glob.glob(os.path.join(folder, pattern))
    # Sort by numeric part of filename
    files.sort()
    return files


def calculate_gif_length(num_frames: int, delay_ms: int) -> float:
    """Calculate GIF length in seconds."""
    return (num_frames * delay_ms) / 1000.0


def format_time_estimate(seconds: float) -> str:
    """Format time estimate in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m {secs}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}m"


def ensure_file_exists(path: str) -> bool:
    """Check if a file exists."""
    return os.path.isfile(path)


def ensure_dir_exists(path: str):
    """Ensure a directory exists, create if it doesn't."""
    os.makedirs(path, exist_ok=True)
