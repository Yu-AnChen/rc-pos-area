# Development Guide

## Setting Up Development Environment

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/yourusername/image-analysis-tool.git
cd image-analysis-tool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Development Dependencies

- **pytest** - Testing framework
- **black** - Code formatter
- **ruff** - Fast Python linter

## Project Structure

```
image-analysis-tool/
├── src/
│   └── image_analysis_tool/
│       ├── __init__.py          # Package initialization and version
│       ├── cli.py               # Command-line interface
│       ├── processor.py         # Image processing and validation
│       └── report.py            # Report generation
├── docs/                        # Documentation
│   ├── INSTALLATION.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── QUICKREF.md
│   └── ...
├── tests/                       # Test files (to be added)
├── pyproject.toml              # Project configuration
├── README.md                   # Main documentation
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT License
└── MANIFEST.in                 # Package data files

```

## Code Style

### Black Formatter

Format code with Black:

```bash
black src/
```

Configuration in `pyproject.toml`:
- Line length: 100
- Target: Python 3.10+

### Ruff Linter

Check code with Ruff:

```bash
ruff check src/
```

Auto-fix issues:

```bash
ruff check --fix src/
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

Edit files in `src/image_analysis_tool/`

### 3. Format and Lint

```bash
black src/
ruff check src/
```

### 4. Test Your Changes

```bash
# Manual testing
image-analysis --help
image-analysis single test_file.xlsx

# Unit tests (when implemented)
pytest tests/
```

### 5. Update Version

Edit version in `src/image_analysis_tool/__init__.py`:

```python
__version__ = "0.2.0"  # Update as needed
```

### 6. Update Changelog

Add entry to `CHANGELOG.md` under `[Unreleased]` section.

### 7. Commit and Push

```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/your-feature-name
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backward-compatible functionality
- **PATCH** version for backward-compatible bug fixes

Examples:
- `0.1.0` → `0.1.1` (bug fix)
- `0.1.1` → `0.2.0` (new feature)
- `0.2.0` → `1.0.0` (breaking change)

## Building the Package

### Build Distribution

```bash
# Install build tools
pip install build

# Build package
python -m build
```

This creates:
- `dist/image_analysis_tool-0.1.0.tar.gz` (source distribution)
- `dist/image_analysis_tool-0.1.0-py3-none-any.whl` (wheel)

### Test Installation

```bash
# Install from local build
pip install dist/image_analysis_tool-0.1.0-py3-none-any.whl

# Verify
image-analysis --help
```

## Publishing

### Test PyPI (recommended first)

```bash
# Install twine
pip install twine

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ image-analysis-tool
```

### Production PyPI

```bash
# Upload to PyPI
twine upload dist/*
```

## Adding Tests

### Create Test Files

```bash
mkdir -p tests
touch tests/test_processor.py
touch tests/test_report.py
touch tests/test_cli.py
```

### Example Test

```python
# tests/test_processor.py
import pytest
from image_analysis_tool.processor import validate_excel_file

def test_validation_missing_file():
    errors = validate_excel_file(Path("nonexistent.xlsx"))
    assert len(errors) > 0
    assert "does not exist" in errors[0]
```

### Run Tests

```bash
pytest tests/
pytest tests/ -v  # Verbose
pytest tests/ --cov=image_analysis_tool  # With coverage
```

## Module Documentation

### Adding Docstrings

Use Google-style docstrings:

```python
def process_single_excel(excel_path: Path, output_dir: Path) -> Path:
    """
    Process a single Excel file.
    
    Args:
        excel_path: Path to input Excel file
        output_dir: Path to output directory
        
    Returns:
        Path to output file
        
    Raises:
        ValidationError: If file validation fails
    """
    pass
```

## Common Tasks

### Running Locally Without Installing

```bash
python -m image_analysis_tool.cli single test.xlsx
```

### Checking Package Metadata

```bash
pip show image-analysis-tool
```

### Cleaning Build Artifacts

```bash
rm -rf build/ dist/ src/*.egg-info
```

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Format and lint code
7. Submit a pull request

## Getting Help

- Check existing documentation in `docs/`
- Review `README.md` for usage examples
- Open an issue on GitHub for bugs or feature requests
