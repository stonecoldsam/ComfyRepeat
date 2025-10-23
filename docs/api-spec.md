# ComfyUI API Specification

This document describes the ComfyUI HTTP API endpoints used by ComfyRepeat.

## Base URL

Default: `http://127.0.0.1:8188`

## Endpoints Used

### POST /prompt

Submit a workflow for execution.

**Request:**
```json
{
  "prompt": {
    "nodes": [...],
    "links": [...],
    ...
  },
  "client_id": "optional_client_id"
}
```

**Response:**
```json
{
  "prompt_id": "unique-prompt-id",
  "number": 123,
  "node_errors": {}
}
```

### GET /history/{prompt_id}

Get execution history and results for a prompt.

**Response:**
```json
{
  "prompt_id": {
    "prompt": [1, {...}],
    "outputs": {
      "node_id": {
        "images": [
          {
            "filename": "ComfyUI_00001.png",
            "subfolder": "",
            "type": "output"
          }
        ]
      }
    },
    "status": {
      "completed": true,
      "messages": []
    }
  }
}
```

### GET /queue

Get current queue status.

**Response:**
```json
{
  "queue_running": [...],
  "queue_pending": [...]
}
```

## Output File Structure

ComfyUI typically saves outputs to:
- `output/{filename}`
- `output/{subfolder}/{filename}`

The filename and subfolder are provided in the history response.

## Workflow JSON Structure

### Node Structure

```json
{
  "id": 1,
  "type": "CLIPTextEncode",
  "title": "Positive Prompt",
  "widgets_values": ["your prompt text here"],
  "inputs": {
    "clip": ["4", 0]
  },
  "outputs": {
    "CONDITIONING": []
  }
}
```

### Key Node Types

- **CLIPTextEncode**: Standard CLIP text encoding
- **CLIPTextEncodeSDXL**: SDXL-specific text encoding
- **PrimitiveNode**: Can contain text or other primitive values
- **LoadImage**: Image input node
- **SaveImage**: Image output node

## Polling Strategy

1. Submit workflow via POST /prompt
2. Get prompt_id from response
3. Poll GET /history/{prompt_id} every 1-2 seconds
4. Check `status.completed` field
5. Extract output images from `outputs` when complete

## Error Handling

- **Connection errors**: Retry with exponential backoff
- **Timeout**: Configurable per-request (default 300s)
- **Node errors**: Check `node_errors` in prompt response
- **Status errors**: Check `status.error` in history response

## Best Practices

1. Always check connection before submitting workflows
2. Use reasonable poll intervals (1-2 seconds)
3. Implement timeout and retry logic
4. Handle missing outputs gracefully
5. Verify file paths before accessing output images
