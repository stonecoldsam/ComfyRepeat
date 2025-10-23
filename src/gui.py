"""
Gradio GUI for ComfyRepeat.
"""
import gradio as gr
import logging
import os
import time
import threading
from typing import Optional, List, Tuple
from PIL import Image

from .workflow_loader import Workflow
from .session import Session
from .comfy_api import ComfyAPI
from .config import Config
from . import utils
from . import gif_builder

logger = logging.getLogger(__name__)


class ComfyRepeatGUI:
    """Gradio-based GUI for ComfyRepeat."""
    
    def __init__(self, config: Config):
        self.config = config
        self.comfy = ComfyAPI(
            base_url=config.get_comfy_url(),
            timeout=config.get("request_timeout", 300)
        )
        
        self.workflow: Optional[Workflow] = None
        self.session: Optional[Session] = None
        
        self.paused = False
        self.stop_requested = False
        self.current_job_id: Optional[str] = None
        self.is_generating = False
        
        self.generation_times = []
    
    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface."""
        with gr.Blocks(title="ComfyRepeat - Interactive Iteration Tool") as interface:
            gr.Markdown("# ComfyRepeat - Interactive ComfyUI Iteration Tool")
            
            with gr.Row():
                # Left column - Image display
                with gr.Column(scale=2):
                    main_image = gr.Image(label="Current Image", type="filepath", height=400)
                    
                    gr.Markdown("### Recent Outputs (Click to Select)")
                    with gr.Row():
                        thumb1 = gr.Image(label="", type="filepath", height=120, interactive=True)
                        thumb2 = gr.Image(label="", type="filepath", height=120, interactive=True)
                        thumb3 = gr.Image(label="", type="filepath", height=120, interactive=True)
                        thumb4 = gr.Image(label="", type="filepath", height=120, interactive=True)
                        thumb5 = gr.Image(label="", type="filepath", height=120, interactive=True)
                    
                    thumbnails = [thumb1, thumb2, thumb3, thumb4, thumb5]
                
                # Right column - Controls
                with gr.Column(scale=1):
                    # Workflow selection
                    gr.Markdown("### Workflow")
                    workflow_path = gr.Textbox(
                        label="Workflow Path",
                        placeholder="Select or enter workflow JSON path",
                        value=self.config.get_last_workflow() or ""
                    )
                    with gr.Row():
                        load_workflow_btn = gr.Button("Load Workflow", variant="primary")
                        browse_workflow_btn = gr.File(label="Browse", file_types=[".json"])
                    
                    workflow_info = gr.Textbox(
                        label="Workflow Info",
                        interactive=False,
                        lines=2
                    )
                    
                    # Prompts
                    gr.Markdown("### Prompts")
                    positive_prompt = gr.Textbox(
                        label="Positive Prompt",
                        lines=4,
                        placeholder="Positive prompt will appear here after loading workflow"
                    )
                    negative_prompt = gr.Textbox(
                        label="Negative Prompt",
                        lines=3,
                        placeholder="Negative prompt will appear here after loading workflow"
                    )
                    
                    # Parameters
                    gr.Markdown("### Parameters")
                    with gr.Row():
                        steps = gr.Number(label="Steps", value=20, precision=0)
                        cfg = gr.Number(label="CFG", value=7.0)
                    with gr.Row():
                        denoise = gr.Slider(label="Denoise", minimum=0, maximum=1, value=1.0, step=0.05)
                        seed = gr.Number(label="Seed", value=-1, precision=0)
                    
                    # Generation controls
                    gr.Markdown("### Controls")
                    with gr.Row():
                        generate_one_btn = gr.Button("Generate One", variant="primary")
                        iterate_count = gr.Number(label="Iterate N Times", value=5, precision=0)
                    with gr.Row():
                        iterate_n_btn = gr.Button("Iterate N", variant="secondary")
                        pause_btn = gr.Button("Pause")
                        resume_btn = gr.Button("Resume", variant="secondary")
                    with gr.Row():
                        finish_btn = gr.Button("Finish & Build GIF", variant="primary")
                        export_btn = gr.Button("Export ZIP")
                    
                    # Session info
                    gr.Markdown("### Session Info")
                    session_info = gr.Textbox(
                        label="Session Status",
                        lines=5,
                        interactive=False
                    )
                    progress_bar = gr.Progress()
                    
                    # Open folder button
                    open_folder_btn = gr.Button("Open Output Folder")
                    
                    # Logs
                    logs = gr.Textbox(label="Logs", lines=3, interactive=False, max_lines=10)
            
            # State variables
            selected_base_image = gr.State(None)
            
            # Event handlers
            def on_browse_workflow(file):
                if file:
                    return file.name
                return ""
            
            browse_workflow_btn.change(
                on_browse_workflow,
                inputs=[browse_workflow_btn],
                outputs=[workflow_path]
            )
            
            def on_load_workflow(path):
                return self.load_workflow(path)
            
            load_workflow_btn.click(
                on_load_workflow,
                inputs=[workflow_path],
                outputs=[workflow_info, positive_prompt, negative_prompt, logs]
            )
            
            def on_generate_one(pos, neg, steps_val, cfg_val, denoise_val, seed_val, base_img):
                return self.generate_one(pos, neg, steps_val, cfg_val, denoise_val, seed_val, base_img)
            
            generate_one_btn.click(
                on_generate_one,
                inputs=[positive_prompt, negative_prompt, steps, cfg, denoise, seed, selected_base_image],
                outputs=[main_image, *thumbnails, session_info, logs]
            )
            
            def on_iterate_n(n, pos, neg, steps_val, cfg_val, denoise_val, seed_val, base_img):
                return self.iterate_n(n, pos, neg, steps_val, cfg_val, denoise_val, seed_val, base_img)
            
            iterate_n_btn.click(
                on_iterate_n,
                inputs=[iterate_count, positive_prompt, negative_prompt, steps, cfg, denoise, seed, selected_base_image],
                outputs=[main_image, *thumbnails, session_info, logs]
            )
            
            pause_btn.click(
                lambda: self.pause(),
                outputs=[logs]
            )
            
            resume_btn.click(
                lambda: self.resume(),
                outputs=[logs]
            )
            
            def on_finish():
                return self.finish_and_build_gif()
            
            finish_btn.click(
                on_finish,
                outputs=[session_info, logs]
            )
            
            def on_export():
                return self.export_session()
            
            export_btn.click(
                on_export,
                outputs=[logs]
            )
            
            def on_open_folder():
                if self.session:
                    folder = self.session.folder
                    return f"Session folder: {folder}"
                return "No active session"
            
            open_folder_btn.click(
                on_open_folder,
                outputs=[logs]
            )
            
            # Thumbnail click handlers
            def select_thumbnail(img_path, thumb_idx):
                if img_path:
                    return img_path, f"Selected thumbnail {thumb_idx} as base image"
                return None, ""
            
            for idx, thumb in enumerate(thumbnails, 1):
                thumb.select(
                    lambda img=thumb, i=idx: select_thumbnail(img, i),
                    inputs=[thumb],
                    outputs=[selected_base_image, logs]
                )
        
        return interface
    
    def load_workflow(self, path: str) -> Tuple:
        """Load a workflow file."""
        try:
            if not path or not os.path.exists(path):
                return ("", "", "", "Error: Workflow file not found")
            
            self.workflow = Workflow(path)
            self.config.set_last_workflow(path)
            
            # Create new session
            workflow_name = os.path.splitext(os.path.basename(path))[0]
            self.session = Session(
                output_root=self.config.get_output_root(),
                workflow_name=workflow_name
            )
            self.session.set_workflow_path(path)
            
            # Get workflow info
            info = self.workflow.get_workflow_info()
            info_text = f"Type: {'I2I' if info['is_i2i'] else 'T2I'}\n"
            info_text += f"Positive node: {info['positive_node_id']}\n"
            info_text += f"Negative node: {info['negative_node_id']}"
            
            pos = self.workflow.get_positive()
            neg = self.workflow.get_negative()
            
            log_msg = f"Loaded workflow: {path}\nSession: {self.session.folder}"
            
            return (info_text, pos, neg, log_msg)
            
        except Exception as e:
            logger.error(f"Failed to load workflow: {e}", exc_info=True)
            return ("", "", "", f"Error loading workflow: {str(e)}")
    
    def generate_one(self, pos: str, neg: str, steps_val: int, cfg_val: float,
                    denoise_val: float, seed_val: int, base_img: Optional[str]) -> Tuple:
        """Generate a single image."""
        try:
            if not self.workflow or not self.session:
                return (None, None, None, None, None, None, "", "Error: Load workflow first")
            
            # Check ComfyUI connection
            if not self.comfy.check_connection():
                return (None, None, None, None, None, None, "", 
                       f"Error: Cannot connect to ComfyUI at {self.comfy.base_url}")
            
            self.is_generating = True
            start_time = time.time()
            
            # Update prompts
            self.workflow.set_positive(pos)
            self.workflow.set_negative(neg)
            
            # Set image input if I2I and base image provided
            if self.workflow.is_i2i() and (base_img or self.session.last_image):
                img_to_use = base_img or self.session.last_image
                self.workflow.set_image_input(img_to_use)
            
            # Get workflow JSON
            workflow_json = self.workflow.get_serializable()
            
            # Submit to ComfyUI
            prompt_id = self.comfy.submit_workflow(workflow_json)
            self.current_job_id = prompt_id
            
            # Poll until done
            result = self.comfy.poll_until_done(prompt_id, poll_interval=1.0)
            
            # Get output image
            if not result["outputs"]:
                return (None, None, None, None, None, None, "",
                       "Error: No outputs from ComfyUI")
            
            output_info = result["outputs"][0]
            # Try to construct full path
            img_path = output_info["path"]
            if not os.path.isabs(img_path):
                # Try common ComfyUI paths
                possible_paths = [
                    img_path,
                    os.path.join(os.getcwd(), img_path),
                    os.path.join("ComfyUI", img_path)
                ]
                for p in possible_paths:
                    if os.path.exists(p):
                        img_path = p
                        break
            
            if not os.path.exists(img_path):
                return (None, None, None, None, None, None, "",
                       f"Error: Output image not found: {img_path}")
            
            # Save frame
            frame_path = self.session.save_frame(
                img_path, pos, neg,
                steps=steps_val, cfg=cfg_val, seed=seed_val, denoise=denoise_val
            )
            
            # Track generation time
            gen_time = time.time() - start_time
            self.generation_times.append(gen_time)
            
            self.is_generating = False
            self.current_job_id = None
            
            # Get recent frames for thumbnails
            recent = self.session.get_recent_frames(5)
            thumbs = recent + [None] * (5 - len(recent))
            
            # Update session info
            info = self.get_session_info()
            
            log_msg = f"Generated frame {self.session.frame_count} in {gen_time:.1f}s"
            
            return (frame_path, *thumbs, info, log_msg)
            
        except Exception as e:
            logger.error(f"Generation failed: {e}", exc_info=True)
            self.is_generating = False
            return (None, None, None, None, None, None, "", f"Error: {str(e)}")
    
    def iterate_n(self, n: int, pos: str, neg: str, steps_val: int, cfg_val: float,
                 denoise_val: float, seed_val: int, base_img: Optional[str]) -> Tuple:
        """Iterate generation N times."""
        try:
            if not self.workflow or not self.session:
                return (None, None, None, None, None, None, "", "Error: Load workflow first")
            
            n = int(n)
            if n <= 0:
                return (None, None, None, None, None, None, "", "Error: N must be > 0")
            
            max_frames = self.config.get("auto_max_frames", 500)
            if self.session.frame_count + n > max_frames:
                return (None, None, None, None, None, None, "",
                       f"Error: Would exceed max frames ({max_frames})")
            
            self.paused = False
            self.stop_requested = False
            
            last_img = base_img
            last_result = None
            
            for i in range(n):
                if self.stop_requested:
                    break
                
                while self.paused and not self.stop_requested:
                    time.sleep(0.2)
                
                if self.stop_requested:
                    break
                
                # Generate one
                result = self.generate_one(pos, neg, steps_val, cfg_val, denoise_val, seed_val, last_img)
                last_result = result
                
                # Use generated image as next base
                if result[0]:  # main_image
                    last_img = result[0]
            
            if last_result:
                return last_result
            else:
                return (None, None, None, None, None, None, "", "Iteration completed")
                
        except Exception as e:
            logger.error(f"Iteration failed: {e}", exc_info=True)
            return (None, None, None, None, None, None, "", f"Error: {str(e)}")
    
    def pause(self) -> str:
        """Pause iteration."""
        self.paused = True
        return "Paused (current generation will complete)"
    
    def resume(self) -> str:
        """Resume iteration."""
        self.paused = False
        return "Resumed"
    
    def finish_and_build_gif(self) -> Tuple[str, str]:
        """Finish session and build GIF."""
        try:
            if not self.session:
                return ("", "Error: No active session")
            
            if self.session.frame_count == 0:
                return ("", "Error: No frames to build GIF")
            
            self.stop_requested = True
            
            # Build GIF
            delay_ms = self.config.get("gif_delay_ms", 100)
            interp_method = self.config.get("interpolation_method", "none")
            
            gif_path = self.session.build_gif(
                delay_ms=delay_ms,
                interpolation=interp_method if interp_method != "none" else None
            )
            
            info = self.get_session_info()
            log_msg = f"Built GIF: {gif_path}"
            
            return (info, log_msg)
            
        except Exception as e:
            logger.error(f"Failed to build GIF: {e}", exc_info=True)
            return ("", f"Error: {str(e)}")
    
    def export_session(self) -> str:
        """Export session as ZIP."""
        try:
            if not self.session:
                return "Error: No active session"
            
            zip_path = self.session.export_zip()
            return f"Exported to: {zip_path}"
            
        except Exception as e:
            logger.error(f"Failed to export session: {e}", exc_info=True)
            return f"Error: {str(e)}"
    
    def get_session_info(self) -> str:
        """Get session information text."""
        if not self.session:
            return "No active session"
        
        info = self.session.get_session_info()
        
        frame_count = info["frame_count"]
        delay_ms = self.config.get("gif_delay_ms", 100)
        gif_length = utils.calculate_gif_length(frame_count, delay_ms)
        
        # Calculate ETA
        eta_text = ""
        if self.generation_times and not self.paused:
            avg_time = sum(self.generation_times) / len(self.generation_times)
            eta_text = f"\nAvg gen time: {avg_time:.1f}s"
        
        status = "Generating" if self.is_generating else ("Paused" if self.paused else "Ready")
        
        text = f"Status: {status}\n"
        text += f"Frames: {frame_count}\n"
        text += f"GIF length: {gif_length:.1f}s\n"
        text += f"Folder: {info['folder']}"
        text += eta_text
        
        return text


def launch_gui(config: Config, share: bool = False):
    """Launch the Gradio GUI."""
    gui = ComfyRepeatGUI(config)
    interface = gui.create_interface()
    interface.launch(share=share, inbrowser=True)
