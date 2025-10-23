# Contributing to ComfyRepeat

Thank you for considering contributing to ComfyRepeat! This document provides guidelines and instructions for contributing.

## Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Add new features
- 🎨 Share example workflows
- 🧪 Write tests

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a new branch for your changes
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ComfyRepeat.git
cd ComfyRepeat

# Install dependencies (including dev dependencies)
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with verbose logging for debugging
python -m src.main --verbose
```

## Code Style

We follow PEP 8 guidelines with some flexibility:

- Line length: 100 characters (not strict)
- Use meaningful variable names
- Add docstrings to functions and classes
- Comment complex logic

### Formatting

```bash
# Format code with black
black src/ tests/

# Check style with flake8
flake8 src/ tests/
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_workflow_loader.py

# Run with coverage
pytest tests/ --cov=src
```

### Writing Tests

- Add tests for new features
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests focused and simple

Example:
```python
def test_feature_name_behavior():
    """Test that feature_name handles case X correctly."""
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = feature_name(input_data)
    
    # Assert
    assert result == expected_value
```

## Pull Request Process

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, focused commits
   - Add tests if applicable
   - Update documentation

3. **Test thoroughly**
   ```bash
   pytest tests/
   ```

4. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update USAGE.md for new features

5. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: short description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **PR Description**
   - Describe what changes you made
   - Explain why you made them
   - Reference any related issues
   - Include screenshots for UI changes

## Commit Message Guidelines

Use clear, descriptive commit messages:

**Good:**
- "Add blend interpolation for GIF builder"
- "Fix prompt detection for SDXL workflows"
- "Update README with installation instructions"

**Not so good:**
- "fix bug"
- "update"
- "changes"

## Feature Requests

Have an idea? Great! Please:

1. Check if it's already been suggested (Issues tab)
2. Open a new issue with:
   - Clear description of the feature
   - Use case / why it's useful
   - Example of how it would work
   - Any implementation ideas (optional)

## Bug Reports

Found a bug? Please:

1. Check if it's already been reported
2. Open a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Your environment (OS, Python version, etc.)
   - Relevant logs (use `--verbose`)

Example:
```markdown
**Bug**: Workflow detection fails for SDXL workflows

**Steps to reproduce**:
1. Load workflow: `my_sdxl_workflow.json`
2. Click "Load Workflow"

**Expected**: Prompt nodes detected

**Actual**: Error "Could not auto-detect prompt nodes"

**Environment**:
- OS: Ubuntu 22.04
- Python: 3.10.8
- ComfyUI: Latest

**Logs**:
```
ERROR - Could not find text nodes
```
```

## Code of Conduct

Be respectful and constructive:
- Be welcoming to newcomers
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

## Project Structure

Understanding the codebase:

```
src/
├── main.py              # Entry point
├── gui.py               # Gradio interface
├── comfy_api.py         # ComfyUI API wrapper
├── workflow_loader.py   # Workflow detection and loading
├── session.py           # Session/frame management
├── gif_builder.py       # GIF creation
├── config.py            # Configuration
└── utils.py             # Utilities

tests/
├── test_workflow_loader.py  # Workflow tests
└── ...                       # More tests

workflows/
├── example_t2i_simple.json  # Example T2I workflow
└── example_i2i_simple.json  # Example I2I workflow
```

## Areas Needing Help

Current priorities:

- 🧪 More comprehensive tests
- 📝 Documentation improvements
- 🎨 More example workflows
- 🌐 Internationalization
- 🚀 Performance optimizations
- 🔌 Plugin system for custom nodes
- 📊 Better progress visualization

## Example Contributions

### Adding a New Feature

1. Create an issue to discuss the feature
2. Get feedback from maintainers
3. Implement in a new branch
4. Add tests
5. Update documentation
6. Submit PR

### Improving Documentation

1. Find areas that need clarification
2. Make improvements
3. Submit PR (no issue needed for docs)

### Sharing Example Workflows

1. Create a workflow in ComfyUI
2. Test it with ComfyRepeat
3. Add to `workflows/` with descriptive name
4. Update `workflows/README.md`
5. Submit PR

## Questions?

- Open an issue with the "question" label
- Check existing issues/discussions
- Review documentation first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to ComfyRepeat! 🙏
