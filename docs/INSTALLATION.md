# Installation Guide

## Requirements

- Python 3.10 or higher
- pip (Python package installer)

## Installation Methods

### Method 1: Install from PyPI (Recommended)

Once published to PyPI:

```bash
pip install image-analysis-tool
```

### Method 2: Install from Source

#### Clone the repository
```bash
git clone https://github.com/yourusername/image-analysis-tool.git
cd image-analysis-tool
```

#### Install in development mode
```bash
pip install -e .
```

#### Or install normally
```bash
pip install .
```

### Method 3: Install from GitHub

```bash
pip install git+https://github.com/yourusername/image-analysis-tool.git
```

## Verify Installation

After installation, verify the tool is available:

```bash
image-analysis --help
```

You should see the help message with available commands.

## Dependencies

The following packages will be installed automatically:

- pandas (>=2.0.0) - Data manipulation
- openpyxl (>=3.1.0) - Excel file handling
- numpy (>=1.24.0) - Numerical operations
- dask-image (>=2023.0.0) - Image processing
- palom (>=2023.0.0) - OME-TIFF pyramid reading
- matplotlib (>=3.7.0) - Color palette support

## Development Installation

For development with additional tools:

```bash
pip install -e ".[dev]"
```

This installs additional packages:
- pytest - Testing framework
- black - Code formatter
- ruff - Fast Python linter

## Troubleshooting

### Import Error: palom

If you encounter issues with palom:

```bash
pip install --upgrade palom
```

### Permission Issues

On Unix/Linux/macOS, you may need to use `--user` flag:

```bash
pip install --user image-analysis-tool
```

Or use a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install image-analysis-tool
```

### Command Not Found

If `image-analysis` command is not found after installation:

1. Check if pip's bin directory is in your PATH
2. Try using the full path: `python -m image_analysis_tool.cli`
3. Or reinstall in a virtual environment

## Updating

To update to the latest version:

```bash
pip install --upgrade image-analysis-tool
```

## Uninstallation

To remove the package:

```bash
pip uninstall image-analysis-tool
```
