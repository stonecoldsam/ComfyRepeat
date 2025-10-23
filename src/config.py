"""
Configuration management for ComfyRepeat.
"""
import json
import os
from typing import Optional


class Config:
    """Configuration manager for ComfyRepeat."""
    
    def __init__(self, config_file: str = ".comfy_repeat_config.json"):
        self.config_file = config_file
        self.data = self._load()
    
    def _load(self) -> dict:
        """Load configuration from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
        
        # Return defaults
        return {
            "last_workflow_path": None,
            "output_root": "outputs",
            "comfy_ui_url": "http://127.0.0.1:8188",
            "auto_max_frames": 500,
            "interpolation_method": "none",
            "interpolation_tool_path": "",
            "gif_delay_ms": 100,
            "default_steps": 20,
            "default_cfg": 7.0,
            "default_denoise": 1.0,
            "poll_interval": 1.0,
            "request_timeout": 300
        }
    
    def save(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.data.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value."""
        self.data[key] = value
        self.save()
    
    def get_last_workflow(self) -> Optional[str]:
        """Get last used workflow path."""
        return self.data.get("last_workflow_path")
    
    def set_last_workflow(self, path: str):
        """Set last used workflow path."""
        self.set("last_workflow_path", path)
    
    def get_comfy_url(self) -> str:
        """Get ComfyUI server URL."""
        return self.data.get("comfy_ui_url", "http://127.0.0.1:8188")
    
    def get_output_root(self) -> str:
        """Get output root directory."""
        return self.data.get("output_root", "outputs")


def save_last_session(workflow_path: str, base_image: Optional[str], 
                     positive: str, negative: str, 
                     session_file: str = ".last_session.json"):
    """Save last session information."""
    data = {
        "workflow_path": workflow_path,
        "base_image": base_image,
        "positive_prompt": positive,
        "negative_prompt": negative
    }
    try:
        with open(session_file, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save session: {e}")


def load_last_session(session_file: str = ".last_session.json") -> Optional[dict]:
    """Load last session information."""
    if os.path.exists(session_file):
        try:
            with open(session_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load session: {e}")
    return None
