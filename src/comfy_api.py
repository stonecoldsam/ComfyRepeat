"""
ComfyUI API wrapper for submitting workflows and polling results.
"""
import requests
import time
import logging
from typing import Optional, Dict, List
import json
import os

logger = logging.getLogger(__name__)


class ComfyAPI:
    """Wrapper for ComfyUI HTTP API."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8188", timeout: int = 300):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def submit_workflow(self, workflow_json: dict, client_id: Optional[str] = None) -> str:
        """
        Submit workflow to ComfyUI.
        
        Args:
            workflow_json: The workflow JSON to submit
            client_id: Optional client ID for WebSocket tracking
            
        Returns:
            prompt_id: The ID of the submitted prompt
        """
        url = f"{self.base_url}/prompt"
        
        payload = {
            "prompt": workflow_json
        }
        if client_id:
            payload["client_id"] = client_id
        
        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            
            if "prompt_id" in result:
                prompt_id = result["prompt_id"]
                logger.info(f"Submitted workflow, prompt_id: {prompt_id}")
                return prompt_id
            else:
                raise RuntimeError(f"No prompt_id in response: {result}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to submit workflow: {e}")
            raise RuntimeError(f"Failed to submit workflow to ComfyUI: {e}")
    
    def poll_until_done(self, prompt_id: str, poll_interval: float = 1.0, 
                       max_retries: int = 3) -> Dict:
        """
        Poll ComfyUI until the prompt is complete.
        
        Args:
            prompt_id: The prompt ID to poll
            poll_interval: Time between polls in seconds
            max_retries: Maximum number of retries on failure
            
        Returns:
            Dictionary containing metadata and output paths
        """
        url = f"{self.base_url}/history/{prompt_id}"
        retries = 0
        
        while True:
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                history = response.json()
                
                if prompt_id in history:
                    prompt_data = history[prompt_id]
                    status = prompt_data.get("status", {})
                    
                    if status.get("completed", False):
                        logger.info(f"Prompt {prompt_id} completed")
                        return self._extract_output_info(prompt_data)
                    elif "error" in status:
                        error_msg = status.get("error", "Unknown error")
                        raise RuntimeError(f"ComfyUI error: {error_msg}")
                
                # Not done yet, keep polling
                time.sleep(poll_interval)
                retries = 0  # Reset retries on successful poll
                
            except requests.exceptions.RequestException as e:
                retries += 1
                if retries >= max_retries:
                    logger.error(f"Failed to poll after {max_retries} retries: {e}")
                    raise RuntimeError(f"Failed to poll ComfyUI: {e}")
                
                logger.warning(f"Poll failed (retry {retries}/{max_retries}): {e}")
                time.sleep(poll_interval * (2 ** retries))  # Exponential backoff
    
    def _extract_output_info(self, prompt_data: dict) -> Dict:
        """Extract output information from prompt data."""
        result = {
            "prompt_id": prompt_data.get("prompt", [None])[0],
            "outputs": [],
            "metadata": {}
        }
        
        # Extract outputs
        outputs = prompt_data.get("outputs", {})
        for node_id, node_output in outputs.items():
            if "images" in node_output:
                for img_info in node_output["images"]:
                    filename = img_info.get("filename")
                    subfolder = img_info.get("subfolder", "")
                    img_type = img_info.get("type", "output")
                    
                    if filename:
                        # Construct the likely file path
                        # ComfyUI typically saves to output/{subfolder}/{filename}
                        if subfolder:
                            file_path = os.path.join("output", subfolder, filename)
                        else:
                            file_path = os.path.join("output", filename)
                        
                        result["outputs"].append({
                            "filename": filename,
                            "subfolder": subfolder,
                            "type": img_type,
                            "path": file_path,
                            "node_id": node_id
                        })
        
        # Extract any metadata from prompt
        if isinstance(prompt_data.get("prompt"), list) and len(prompt_data["prompt"]) > 1:
            extra_data = prompt_data["prompt"][1]
            result["metadata"] = extra_data
        
        return result
    
    def get_recent_outputs(self, limit: int = 5) -> List[str]:
        """
        Get recent output file paths.
        
        Args:
            limit: Maximum number of outputs to return
            
        Returns:
            List of file paths
        """
        # This is a simple implementation that assumes ComfyUI output folder
        output_dir = "output"
        if not os.path.exists(output_dir):
            return []
        
        files = []
        for root, dirs, filenames in os.walk(output_dir):
            for filename in filenames:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    files.append(os.path.join(root, filename))
        
        # Sort by modification time, most recent first
        files.sort(key=lambda x: os.path.getmtime(x) if os.path.exists(x) else 0, 
                  reverse=True)
        
        return files[:limit]
    
    def get_queue_info(self) -> Dict:
        """Get current queue information."""
        url = f"{self.base_url}/queue"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to get queue info: {e}")
            return {}
    
    def check_connection(self) -> bool:
        """Check if ComfyUI server is reachable."""
        try:
            response = self.session.get(self.base_url, timeout=5)
            return response.status_code in [200, 301, 302]
        except:
            return False
