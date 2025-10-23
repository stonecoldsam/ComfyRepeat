"""
Tests for workflow loader and lazy detection.
"""
import json
import os
import tempfile
import pytest
from src.workflow_loader import Workflow


def create_test_workflow(nodes):
    """Helper to create a test workflow JSON."""
    return {
        "nodes": nodes,
        "links": [],
        "groups": [],
        "config": {},
        "version": 0.4
    }


def test_lazy_detect_by_title():
    """Test detection by node title (Rule 1)."""
    nodes = [
        {
            "id": 1,
            "type": "CLIPTextEncode",
            "title": "Positive Prompt",
            "widgets_values": ["a beautiful landscape"],
            "inputs": {"clip": ["2", 0]},
            "outputs": {}
        },
        {
            "id": 2,
            "type": "CLIPTextEncode",
            "title": "Negative Prompt",
            "widgets_values": ["blurry, low quality"],
            "inputs": {"clip": ["2", 0]},
            "outputs": {}
        },
        {
            "id": 3,
            "type": "CheckpointLoaderSimple",
            "title": "Load Model",
            "widgets_values": ["model.safetensors"],
            "inputs": {},
            "outputs": {}
        }
    ]
    
    workflow_data = create_test_workflow(nodes)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(workflow_data, f)
        temp_path = f.name
    
    try:
        workflow = Workflow(temp_path)
        
        assert workflow.positive_node is not None
        assert workflow.negative_node is not None
        assert workflow.positive_node["id"] == 1
        assert workflow.negative_node["id"] == 2
        
        assert workflow.get_positive() == "a beautiful landscape"
        assert workflow.get_negative() == "blurry, low quality"
        
    finally:
        os.unlink(temp_path)


def test_lazy_detect_fallback():
    """Test fallback detection (Rule 2)."""
    nodes = [
        {
            "id": 10,
            "type": "PrimitiveNode",
            "title": "Text Node 1",
            "widgets_values": ["first text node"],
            "inputs": {},
            "outputs": {}
        },
        {
            "id": 5,
            "type": "PrimitiveNode",
            "title": "Text Node 2",
            "widgets_values": ["second text node"],
            "inputs": {},
            "outputs": {}
        },
        {
            "id": 20,
            "type": "SaveImage",
            "title": "Save",
            "widgets_values": ["image"],
            "inputs": {},
            "outputs": {}
        }
    ]
    
    workflow_data = create_test_workflow(nodes)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(workflow_data, f)
        temp_path = f.name
    
    try:
        workflow = Workflow(temp_path)
        
        # Should detect by order (sorted by ID)
        assert workflow.positive_node is not None
        assert workflow.negative_node is not None
        
        # IDs should be 5 and 10 (sorted order)
        assert workflow.positive_node["id"] == 5
        assert workflow.negative_node["id"] == 10
        
    finally:
        os.unlink(temp_path)


def test_set_prompts():
    """Test setting prompt text."""
    nodes = [
        {
            "id": 1,
            "type": "CLIPTextEncode",
            "title": "positive",
            "widgets_values": ["original positive"],
            "inputs": {},
            "outputs": {}
        },
        {
            "id": 2,
            "type": "CLIPTextEncode",
            "title": "negative",
            "widgets_values": ["original negative"],
            "inputs": {},
            "outputs": {}
        }
    ]
    
    workflow_data = create_test_workflow(nodes)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(workflow_data, f)
        temp_path = f.name
    
    try:
        workflow = Workflow(temp_path)
        
        # Change prompts
        workflow.set_positive("new positive prompt")
        workflow.set_negative("new negative prompt")
        
        assert workflow.get_positive() == "new positive prompt"
        assert workflow.get_negative() == "new negative prompt"
        
        # Verify base prompts are preserved
        assert workflow.base_positive == "original positive"
        assert workflow.base_negative == "original negative"
        
    finally:
        os.unlink(temp_path)


def test_image_node_detection():
    """Test image node detection for I2I."""
    nodes = [
        {
            "id": 1,
            "type": "CLIPTextEncode",
            "title": "positive",
            "widgets_values": ["test"],
            "inputs": {},
            "outputs": {}
        },
        {
            "id": 2,
            "type": "CLIPTextEncode",
            "title": "negative",
            "widgets_values": ["test"],
            "inputs": {},
            "outputs": {}
        },
        {
            "id": 3,
            "type": "LoadImage",
            "title": "Load Image",
            "widgets_values": ["image.png"],
            "inputs": {},
            "outputs": {}
        }
    ]
    
    workflow_data = create_test_workflow(nodes)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(workflow_data, f)
        temp_path = f.name
    
    try:
        workflow = Workflow(temp_path)
        
        assert workflow.is_i2i() is True
        assert workflow.image_node is not None
        assert workflow.image_node["id"] == 3
        
    finally:
        os.unlink(temp_path)


def test_no_image_node_t2i():
    """Test T2I workflow (no image node)."""
    nodes = [
        {
            "id": 1,
            "type": "CLIPTextEncode",
            "title": "positive",
            "widgets_values": ["test"],
            "inputs": {},
            "outputs": {}
        },
        {
            "id": 2,
            "type": "CLIPTextEncode",
            "title": "negative",
            "widgets_values": ["test"],
            "inputs": {},
            "outputs": {}
        }
    ]
    
    workflow_data = create_test_workflow(nodes)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(workflow_data, f)
        temp_path = f.name
    
    try:
        workflow = Workflow(temp_path)
        
        assert workflow.is_i2i() is False
        assert workflow.image_node is None
        
    finally:
        os.unlink(temp_path)


def test_get_serializable():
    """Test getting serializable workflow copy."""
    nodes = [
        {
            "id": 1,
            "type": "CLIPTextEncode",
            "title": "positive",
            "widgets_values": ["original"],
            "inputs": {},
            "outputs": {}
        },
        {
            "id": 2,
            "type": "CLIPTextEncode",
            "title": "negative",
            "widgets_values": ["original"],
            "inputs": {},
            "outputs": {}
        }
    ]
    
    workflow_data = create_test_workflow(nodes)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(workflow_data, f)
        temp_path = f.name
    
    try:
        workflow = Workflow(temp_path)
        workflow.set_positive("modified")
        
        # Get serializable copy
        copy = workflow.get_serializable()
        
        # Check it's a proper copy
        assert copy is not workflow.raw
        assert copy["nodes"][0]["widgets_values"][0] == "modified"
        
    finally:
        os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
