"""
Session folder and metadata management.
"""
import os
import json
import shutil
import logging
import zipfile
from typing import Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class Session:
    """Manages a single iteration session."""
    
    def __init__(self, output_root: str = "outputs", workflow_name: str = "unknown"):
        self.output_root = output_root
        self.workflow_name = workflow_name
        self.folder = self._create_session_folder()
        self.frame_index = 0
        self.last_image = None
        self.frames = []
        self.metadata = {
            "workflow_name": workflow_name,
            "workflow_path": None,
            "created_at": datetime.now().isoformat(),
            "frames": [],
            "interpolation_used": False,
            "notes": ""
        }
        logger.info(f"Created session: {self.folder}")
    
    def _create_session_folder(self) -> str:
        """Create a timestamped session folder."""
        os.makedirs(self.output_root, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = os.path.join(self.output_root, f"session_{timestamp}")
        os.makedirs(folder, exist_ok=True)
        return folder
    
    def save_frame(self, src_image_path: str, prompt_pos: str, prompt_neg: str,
                   steps: Optional[int] = None, cfg: Optional[float] = None,
                   seed: Optional[int] = None, denoise: Optional[float] = None) -> str:
        """
        Save a frame to the session folder.
        
        Args:
            src_image_path: Path to the source image
            prompt_pos: Positive prompt used
            prompt_neg: Negative prompt used
            steps: Number of steps
            cfg: CFG scale
            seed: Seed value
            denoise: Denoise strength
            
        Returns:
            Path to the saved frame
        """
        self.frame_index += 1
        frame_filename = f"frame_{self.frame_index:03d}.png"
        frame_path = os.path.join(self.folder, frame_filename)
        
        # Copy image to session folder
        try:
            shutil.copy2(src_image_path, frame_path)
            logger.info(f"Saved frame {self.frame_index}: {frame_path}")
        except Exception as e:
            logger.error(f"Failed to save frame: {e}")
            raise
        
        # Update last image
        self.last_image = frame_path
        self.frames.append(frame_path)
        
        # Add frame metadata
        frame_meta = {
            "frame_number": self.frame_index,
            "filename": frame_filename,
            "timestamp": datetime.now().isoformat(),
            "prompt_positive": prompt_pos,
            "prompt_negative": prompt_neg,
            "steps": steps,
            "cfg": cfg,
            "seed": seed,
            "denoise": denoise
        }
        self.metadata["frames"].append(frame_meta)
        
        # Save metadata
        self._save_metadata()
        
        return frame_path
    
    def _save_metadata(self):
        """Save metadata to JSON file."""
        metadata_path = os.path.join(self.folder, "metadata.json")
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
    
    def set_workflow_path(self, path: str):
        """Set the workflow path in metadata."""
        self.metadata["workflow_path"] = path
        self._save_metadata()
    
    def set_notes(self, notes: str):
        """Set session notes."""
        self.metadata["notes"] = notes
        self._save_metadata()
    
    def build_gif(self, delay_ms: int = 100, interpolation: Optional[str] = None,
                  interpolation_params: Optional[Dict] = None) -> str:
        """
        Build GIF from session frames.
        
        Args:
            delay_ms: Delay between frames in milliseconds
            interpolation: Interpolation method ('none', 'blend', 'rife')
            interpolation_params: Parameters for interpolation
            
        Returns:
            Path to the generated GIF
        """
        from . import gif_builder
        
        gif_path = os.path.join(self.folder, "evolution.gif")
        
        gif_builder.build_gif_from_folder(
            self.folder,
            gif_path,
            delay_ms=delay_ms,
            interpolation=interpolation,
            interpolation_params=interpolation_params
        )
        
        self.metadata["interpolation_used"] = interpolation not in [None, "none"]
        self._save_metadata()
        
        logger.info(f"Generated GIF: {gif_path}")
        return gif_path
    
    def export_zip(self, zip_path: Optional[str] = None) -> str:
        """
        Export session as a ZIP file.
        
        Args:
            zip_path: Optional custom path for the ZIP file
            
        Returns:
            Path to the created ZIP file
        """
        if not zip_path:
            zip_path = f"{self.folder}.zip"
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(self.folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.folder)
                        zipf.write(file_path, arcname)
            
            logger.info(f"Exported session to: {zip_path}")
            return zip_path
            
        except Exception as e:
            logger.error(f"Failed to export session: {e}")
            raise
    
    def get_frame_count(self) -> int:
        """Get the number of frames in this session."""
        return self.frame_index
    
    def get_recent_frames(self, limit: int = 5) -> List[str]:
        """Get the most recent frames."""
        return self.frames[-limit:] if self.frames else []
    
    def get_session_info(self) -> Dict:
        """Get session information summary."""
        return {
            "folder": self.folder,
            "frame_count": self.frame_index,
            "workflow_name": self.workflow_name,
            "last_image": self.last_image,
            "created_at": self.metadata["created_at"]
        }
