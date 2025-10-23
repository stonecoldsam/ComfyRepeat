"""
ComfyRepeat - Interactive GUI controller for ComfyUI iterative image evolution.
"""

__version__ = "0.1.0"
__author__ = "ComfyRepeat Contributors"
__description__ = "Interactive GUI controller for ComfyUI that guides iterative image evolution"

from .config import Config
from .workflow_loader import Workflow
from .session import Session
from .comfy_api import ComfyAPI
from . import utils
from . import gif_builder

__all__ = [
    "Config",
    "Workflow",
    "Session",
    "ComfyAPI",
    "utils",
    "gif_builder"
]
