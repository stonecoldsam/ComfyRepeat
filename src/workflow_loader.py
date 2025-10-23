"""
Workflow loader with lazy-as-fuck prompt node detection.
"""
import json
import logging
import copy
from typing import Optional, Tuple, Dict, List

logger = logging.getLogger(__name__)


class Workflow:
    """ComfyUI workflow loader and manager."""
    
    # Node types that typically contain text prompts
    TEXT_NODE_TYPES = {
        "PrimitiveNode",
        "CLIPTextEncode",
        "CLIPTextEncodeSDXL",
        "CLIPTextEncodeSDXLRefiner"
    }
    
    # Node types that typically handle image inputs
    IMAGE_NODE_TYPES = {
        "LoadImage",
        "LoadImageOutput",
        "ImageLoader",
        "ImageScaleToTotalPixels"
    }
    
    def __init__(self, path: str):
        self.path = path
        self.raw = self._load_json(path)
        self.node_map = {node["id"]: node for node in self.raw.get("nodes", [])}
        
        self.positive_node = None
        self.negative_node = None
        self.image_node = None
        
        self.base_positive = ""
        self.base_negative = ""
        
        # Detect nodes
        self.detect_prompt_nodes_lazy()
        self.detect_image_node()
        
        # Store base prompts
        self.base_positive = self.get_positive()
        self.base_negative = self.get_negative()
    
    def _load_json(self, path: str) -> dict:
        """Load workflow JSON from file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load workflow from {path}: {e}")
    
    def detect_prompt_nodes_lazy(self):
        """
        Lazy-as-fuck detection of positive and negative prompt nodes.
        
        Rules:
        1. Search for nodes with title containing "positive" or "negative"
        2. Fallback: Get text-bearing nodes, sort by appearance, assign first two
        """
        nodes = self.raw.get("nodes", [])
        pos = None
        neg = None
        
        # Rule 1: Title-based detection
        for node in nodes:
            title = node.get("title", "").lower()
            if "positive" in title and not pos:
                pos = node
                logger.info(f"Found positive node by title: {node.get('id')}")
            elif "negative" in title and not neg:
                neg = node
                logger.info(f"Found negative node by title: {node.get('id')}")
        
        # Rule 2: Fallback to text-bearing nodes
        if not pos or not neg:
            text_nodes = self._get_text_nodes()
            
            if not pos and len(text_nodes) >= 1:
                pos = text_nodes[0]
                logger.info(f"Found positive node by fallback: {pos.get('id')}")
            
            if not neg and len(text_nodes) >= 2:
                neg = text_nodes[1]
                logger.info(f"Found negative node by fallback: {neg.get('id')}")
        
        if not pos or not neg:
            raise RuntimeError(
                "Could not auto-detect prompt nodes. "
                "Please name nodes 'positive' and 'negative' in your workflow."
            )
        
        self.positive_node = pos
        self.negative_node = neg
    
    def _get_text_nodes(self) -> List[dict]:
        """Get nodes that contain text prompts, sorted by appearance."""
        text_nodes = []
        
        for node in self.raw.get("nodes", []):
            node_type = node.get("type", "")
            
            # Check if it's a known text node type
            if node_type in self.TEXT_NODE_TYPES:
                # Verify it has text content
                if self._has_text_content(node):
                    text_nodes.append(node)
        
        # Sort by node id to maintain deterministic order
        text_nodes.sort(key=lambda n: n.get("id", 0))
        
        return text_nodes
    
    def _has_text_content(self, node: dict) -> bool:
        """Check if a node has text content."""
        # Check widgets_values
        widgets = node.get("widgets_values")
        if widgets and len(widgets) > 0 and isinstance(widgets[0], str):
            return True
        
        # Check inputs
        inputs = node.get("inputs", {})
        if isinstance(inputs, dict):
            for key in ["text", "text_g", "text_l"]:
                if key in inputs and isinstance(inputs[key], str):
                    return True
        
        return False
    
    def detect_image_node(self):
        """Detect image input node for I2I workflows."""
        nodes = self.raw.get("nodes", [])
        
        for node in nodes:
            node_type = node.get("type", "")
            if node_type in self.IMAGE_NODE_TYPES:
                self.image_node = node
                logger.info(f"Found image node: {node.get('id')} ({node_type})")
                break
    
    def is_i2i(self) -> bool:
        """Check if this is an I2I workflow (has image input)."""
        return self.image_node is not None
    
    def get_positive(self) -> str:
        """Get current positive prompt text."""
        return self._get_node_text(self.positive_node)
    
    def get_negative(self) -> str:
        """Get current negative prompt text."""
        return self._get_node_text(self.negative_node)
    
    def _get_node_text(self, node: Optional[dict]) -> str:
        """Extract text from a node."""
        if not node:
            return ""
        
        # Try widgets_values first
        widgets = node.get("widgets_values")
        if widgets and len(widgets) > 0 and isinstance(widgets[0], str):
            return widgets[0]
        
        # Try inputs
        inputs = node.get("inputs", {})
        if isinstance(inputs, dict):
            for key in ["text", "text_g", "text_l"]:
                if key in inputs and isinstance(inputs[key], str):
                    return inputs[key]
        
        return ""
    
    def set_positive(self, new_text: str):
        """Set positive prompt text."""
        self._set_node_text(self.positive_node, new_text)
    
    def set_negative(self, new_text: str):
        """Set negative prompt text."""
        self._set_node_text(self.negative_node, new_text)
    
    def _set_node_text(self, node: Optional[dict], new_text: str):
        """Set text in a node."""
        if not node:
            return
        
        # Try widgets_values first
        if "widgets_values" in node and len(node["widgets_values"]) > 0:
            node["widgets_values"][0] = new_text
            return
        
        # Try inputs
        inputs = node.get("inputs", {})
        if isinstance(inputs, dict):
            for key in ["text", "text_g", "text_l"]:
                if key in inputs:
                    inputs[key] = new_text
                    return
            
            # If no text key exists, try to add one
            if "text" not in inputs:
                inputs["text"] = new_text
                return
        
        # Last resort: create widgets_values
        if "widgets_values" not in node:
            node["widgets_values"] = [new_text]
        else:
            node["widgets_values"][0] = new_text
    
    def set_image_input(self, image_path: str):
        """Set image input path for I2I workflows."""
        if not self.image_node:
            logger.warning("No image node detected, cannot set image input")
            return
        
        node = self.image_node
        
        # Try widgets_values (common for LoadImage)
        if "widgets_values" in node:
            if not node["widgets_values"]:
                node["widgets_values"] = [image_path]
            else:
                node["widgets_values"][0] = image_path
            logger.info(f"Set image via widgets_values: {image_path}")
            return
        
        # Try inputs
        inputs = node.get("inputs", {})
        if isinstance(inputs, dict):
            for key in ["image", "upload", "filename", "file"]:
                if key in inputs:
                    inputs[key] = image_path
                    logger.info(f"Set image via inputs[{key}]: {image_path}")
                    return
            
            # If no known key, add "image"
            inputs["image"] = image_path
            logger.info(f"Set image via new inputs['image']: {image_path}")
            return
        
        # Create widgets_values as last resort
        node["widgets_values"] = [image_path]
        logger.info(f"Set image via new widgets_values: {image_path}")
    
    def get_serializable(self) -> dict:
        """Get a deep copy of the workflow ready for posting to ComfyUI."""
        return copy.deepcopy(self.raw)
    
    def get_workflow_info(self) -> Dict:
        """Get workflow information summary."""
        return {
            "path": self.path,
            "is_i2i": self.is_i2i(),
            "positive_node_id": self.positive_node.get("id") if self.positive_node else None,
            "negative_node_id": self.negative_node.get("id") if self.negative_node else None,
            "image_node_id": self.image_node.get("id") if self.image_node else None,
            "base_positive": self.base_positive,
            "base_negative": self.base_negative
        }
