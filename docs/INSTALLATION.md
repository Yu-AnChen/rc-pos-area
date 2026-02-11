# Installation Guide

## Requirements

- Python 3.10 or higher
- pip (Python package installer)

## Installation Methods

### Method 1: Install from PyPI (Recommended)

Once published to PyPI:

```bash
pip install rc-pos-area
```

### Method 2: Install from Source

#### Clone the repository
```bash
git clone https://github.com/yu-anchen/rc-pos-area.git
cd rc-pos-area
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
pip install git+https://github.com/yu-anchen/rc-pos-area.git
```

## Verify Installation

After installation, verify the tool is available:

```bash
pos-area --help
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
pip install --user rc-pos-area
```

Or use a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install rc-pos-area
```

### Command Not Found

If `pos-area` command is not found after installation:

1. Check if pip's bin directory is in your PATH
2. Try using the full path: `python -m rc_pos_area.cli`
3. Or reinstall in a virtual environment

## Updating

To update to the latest version:

```bash
pip install --upgrade rc-pos-area
```

## Uninstallation

To remove the package:

```bash
pip uninstall rc-pos-area
```
