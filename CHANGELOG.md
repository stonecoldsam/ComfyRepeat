# Changelog

All notable changes to ComfyRepeat will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-10-23

### Added
- Initial release of ComfyRepeat
- Interactive Gradio GUI for iterative image generation
- Support for both T2I (text-to-image) and I2I (image-to-image) workflows
- Lazy-as-fuck automatic detection of prompt nodes in workflows
- Session management with frame numbering and metadata tracking
- GIF generation from iteration frames
- Optional frame interpolation support (blend and RIFE)
- Pause/Resume functionality for mid-iteration prompt editing
- Recent frame thumbnails with click-to-select functionality
- Configurable parameters (steps, CFG, denoise, seed)
- Session export to ZIP files
- Comprehensive metadata JSON for each session
- Configuration persistence across sessions
- Command-line interface with multiple options
- Example T2I and I2I workflow files
- Complete test suite for workflow detection
- Extensive documentation:
  - README with features and quick start
  - QUICKSTART guide for new users
  - Detailed USAGE guide
  - API specification documentation
  - Contributing guidelines
  - MIT License

### Features
- **Workflow Detection**: Automatically detects positive/negative prompt nodes
- **Session Management**: Organized output folders with metadata
- **GIF Builder**: Creates animated GIFs with optional interpolation
- **Interactive GUI**: Easy-to-use Gradio interface
- **Flexible Configuration**: JSON-based config with CLI overrides
- **Error Handling**: Robust retry logic and user-friendly error messages
- **Progress Tracking**: Real-time session info and generation statistics

### Technical Details
- Python 3.10+ support
- Gradio 4.0+ for GUI
- Pillow for image processing
- Requests for ComfyUI API communication
- Comprehensive test coverage with pytest
- Clean, modular architecture
- Type hints throughout codebase

## [Unreleased]

### Planned Features
- Headless mode for CLI-only operation
- Additional interpolation methods
- Batch processing support
- Custom node type support
- Real-time WebSocket updates
- Advanced parameter sweeps
- Workflow templates
- Cloud storage integration
- Multi-language support
- Plugin system

### Known Issues
- Headless mode not yet implemented
- RIFE interpolation requires external tool installation
- Limited to single workflow per session
- No undo/redo for generations

---

## Release Notes Format

### Added
New features.

### Changed
Changes in existing functionality.

### Deprecated
Soon-to-be removed features.

### Removed
Removed features.

### Fixed
Bug fixes.

### Security
Security fixes or improvements.
