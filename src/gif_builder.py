"""
GIF building with optional interpolation/blending.
"""
import os
import glob
import logging
import subprocess
from typing import Optional, Dict, List
from PIL import Image

logger = logging.getLogger(__name__)


def build_gif_from_folder(folder: str, out_filename: str = "evolution.gif",
                         delay_ms: int = 100, interpolation: Optional[str] = None,
                         interpolation_params: Optional[Dict] = None) -> str:
    """
    Build GIF from frames in a folder.
    
    Args:
        folder: Path to folder containing frame_*.png files
        out_filename: Output filename (can be full path)
        delay_ms: Delay between frames in milliseconds
        interpolation: Interpolation method ('none', 'blend', 'rife')
        interpolation_params: Parameters for interpolation
        
    Returns:
        Path to the created GIF
    """
    # Get sorted frame files
    frame_files = sorted(glob.glob(os.path.join(folder, "frame_*.png")))
    
    if not frame_files:
        raise ValueError(f"No frames found in {folder}")
    
    logger.info(f"Building GIF from {len(frame_files)} frames")
    
    # Load frames
    frames = []
    for frame_file in frame_files:
        try:
            img = Image.open(frame_file)
            frames.append(img.convert("RGB"))
        except Exception as e:
            logger.warning(f"Failed to load frame {frame_file}: {e}")
    
    if not frames:
        raise ValueError("No valid frames could be loaded")
    
    # Apply interpolation if requested
    if interpolation == "blend":
        params = interpolation_params or {}
        blend_steps = params.get("blend_steps", 2)
        frames = apply_blend_interpolation(frames, blend_steps)
        logger.info(f"Applied blend interpolation with {blend_steps} steps")
    
    elif interpolation == "rife":
        params = interpolation_params or {}
        rife_path = params.get("rife_path", "rife-ncnn-vulkan")
        frames = apply_rife_interpolation(frame_files, folder, rife_path)
        logger.info("Applied RIFE interpolation")
    
    # Ensure output path is absolute
    if not os.path.isabs(out_filename):
        out_filename = os.path.join(folder, out_filename)
    
    # Save GIF
    try:
        frames[0].save(
            out_filename,
            save_all=True,
            append_images=frames[1:],
            duration=delay_ms,
            loop=0,
            optimize=False
        )
        logger.info(f"Saved GIF to: {out_filename}")
        return out_filename
    except Exception as e:
        logger.error(f"Failed to save GIF: {e}")
        raise


def apply_blend_interpolation(frames: List[Image.Image], blend_steps: int = 2) -> List[Image.Image]:
    """
    Apply crossfade blending between frames.
    
    Args:
        frames: List of PIL Image objects
        blend_steps: Number of blend steps between each frame pair
        
    Returns:
        List of frames with blended transitions
    """
    if len(frames) < 2:
        return frames
    
    result = []
    
    for i in range(len(frames) - 1):
        frame_a = frames[i].convert("RGBA")
        frame_b = frames[i + 1].convert("RGBA")
        
        # Add the first frame
        result.append(frames[i])
        
        # Add blended frames
        for step in range(1, blend_steps + 1):
            alpha = step / (blend_steps + 1)
            blended = Image.blend(frame_a, frame_b, alpha)
            result.append(blended.convert("RGB"))
    
    # Add the last frame
    result.append(frames[-1])
    
    return result


def apply_rife_interpolation(frame_files: List[str], folder: str, 
                            rife_path: str = "rife-ncnn-vulkan") -> List[Image.Image]:
    """
    Apply RIFE interpolation using external tool.
    
    Args:
        frame_files: List of frame file paths
        folder: Working folder
        rife_path: Path to RIFE executable
        
    Returns:
        List of interpolated frames
    """
    # Create temporary directory for RIFE output
    rife_output = os.path.join(folder, "rife_output")
    os.makedirs(rife_output, exist_ok=True)
    
    try:
        # Run RIFE
        # Note: This is a placeholder - actual RIFE command may vary
        cmd = [rife_path, "-i", folder, "-o", rife_output, "-s", "2"]
        
        logger.info(f"Running RIFE: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            logger.warning(f"RIFE failed: {result.stderr}")
            # Fall back to original frames
            return [Image.open(f).convert("RGB") for f in frame_files]
        
        # Load interpolated frames
        interp_files = sorted(glob.glob(os.path.join(rife_output, "*.png")))
        if interp_files:
            return [Image.open(f).convert("RGB") for f in interp_files]
        else:
            logger.warning("No RIFE output found, using original frames")
            return [Image.open(f).convert("RGB") for f in frame_files]
    
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        logger.warning(f"RIFE interpolation failed: {e}, using original frames")
        return [Image.open(f).convert("RGB") for f in frame_files]


def estimate_gif_size(num_frames: int, delay_ms: int) -> Dict[str, float]:
    """
    Estimate GIF properties.
    
    Args:
        num_frames: Number of frames
        delay_ms: Delay per frame in milliseconds
        
    Returns:
        Dictionary with duration and fps
    """
    duration_seconds = (num_frames * delay_ms) / 1000.0
    fps = 1000.0 / delay_ms if delay_ms > 0 else 0
    
    return {
        "duration_seconds": duration_seconds,
        "fps": fps,
        "num_frames": num_frames
    }
