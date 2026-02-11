# Python Package Structure Summary

## Package Information

- **Name**: `image-analysis-tool`
- **Version**: 0.1.0 (dynamically loaded from `__init__.py`)
- **Python Requirements**: >=3.10
- **Build System**: hatchling (modern, PEP 517 compliant)
- **License**: MIT

## Package Structure

```
image-analysis-tool/
├── src/                                    # Source code (src layout)
│   └── image_analysis_tool/
│       ├── __init__.py                     # Package init with version
│       ├── cli.py                          # CLI entry point
│       ├── processor.py                    # Image processing module
│       └── report.py                       # Report generation module
│
├── docs/                                   # Documentation
│   ├── INSTALLATION.md                     # Installation guide
│   ├── QUICKSTART.md                       # Quick start guide
│   ├── DEVELOPMENT.md                      # Development guide
│   ├── QUICKREF.md                         # Quick reference
│   ├── IMPLEMENTATION_SUMMARY.md           # Technical details
│   ├── CHANNEL_INDEXING_FIX.md            # Channel indexing notes
│   └── TISSUE_REGION_FEATURE.md           # Tissue region feature
│
├── tests/                                  # Tests (placeholder)
│   └── (to be added)
│
├── pyproject.toml                          # Modern package configuration
├── setup.py                                # Backward compatibility
├── MANIFEST.in                             # Package data inclusion
├── README.md                               # Main documentation
├── CHANGELOG.md                            # Version history
├── LICENSE                                 # MIT License
└── .gitignore                             # Git ignore rules
```

## Key Files Explained

### pyproject.toml

Modern Python packaging configuration following PEP 517/518:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "image-analysis-tool"
dynamic = ["version"]
requires-python = ">=3.10"
dependencies = [...]

[project.scripts]
image-analysis = "image_analysis_tool.cli:main"
```

**Features**:
- Dynamic versioning from `__init__.py`
- Minimal configuration
- hatchling build backend (fast, modern)
- Automatic script generation
- Dev dependencies in optional-dependencies

### src/image_analysis_tool/__init__.py

```python
__version__ = "0.1.0"

from image_analysis_tool.processor import process_single_excel, validate_excel_file
from image_analysis_tool.report import generate_summary_report

__all__ = [...]
```

**Purpose**:
- Version string (used by hatchling)
- Package-level imports
- Public API definition

### Source Layout (src/)

Benefits of src/ layout:
- Prevents accidental imports from source
- Clearer separation between source and tests
- Forces proper installation for testing
- Industry best practice

## Installation Methods

### End Users

```bash
# From PyPI (when published)
pip install image-analysis-tool

# From GitHub
pip install git+https://github.com/user/image-analysis-tool.git

# From local directory
pip install .
```

### Developers

```bash
# Editable install with dev dependencies
pip install -e ".[dev]"
```

## CLI Entry Point

The package creates a `image-analysis` command:

```bash
image-analysis single file.xlsx
image-analysis batch ./data/
image-analysis report ./results/
```

Configured in `pyproject.toml`:
```toml
[project.scripts]
image-analysis = "image_analysis_tool.cli:main"
```

## Building the Package

### Using build

```bash
pip install build
python -m build
```

Creates:
- `dist/image_analysis_tool-0.1.0.tar.gz` (source)
- `dist/image_analysis_tool-0.1.0-py3-none-any.whl` (wheel)

### What Gets Included

From `MANIFEST.in`:
- README.md
- LICENSE
- CHANGELOG.md
- All documentation in docs/

From hatchling defaults:
- All Python files in src/image_analysis_tool/
- pyproject.toml metadata

## Version Management

### Current: 0.1.0

Version is defined in `src/image_analysis_tool/__init__.py`:
```python
__version__ = "0.1.0"
```

### To Update Version

1. Edit `src/image_analysis_tool/__init__.py`
2. Update `CHANGELOG.md` with changes
3. Commit and tag: `git tag v0.2.0`
4. Build and publish

## Dependencies

### Required (automatically installed)

- pandas >= 2.0.0
- openpyxl >= 3.1.0
- numpy >= 1.24.0
- dask-image >= 2023.0.0
- palom >= 2023.0.0
- matplotlib >= 3.7.0

### Optional (dev)

- pytest >= 7.0
- black >= 23.0
- ruff >= 0.1.0

## Code Quality

### Formatting: Black

```bash
black src/
```

Config in pyproject.toml:
- Line length: 100
- Target: Python 3.10

### Linting: Ruff

```bash
ruff check src/
ruff check --fix src/
```

Config in pyproject.toml:
- Line length: 100
- Selected rules: E, W, F, I, B, C4

## Publishing Workflow

### 1. Update Version

Edit `__init__.py` and `CHANGELOG.md`

### 2. Build

```bash
python -m build
```

### 3. Test on Test PyPI

```bash
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ image-analysis-tool
```

### 4. Publish to PyPI

```bash
twine upload dist/*
```

### 5. Tag Release

```bash
git tag v0.1.0
git push origin v0.1.0
```

## API Usage

Besides CLI, package can be used as a library:

```python
from image_analysis_tool import process_single_excel, validate_excel_file
from pathlib import Path

# Validate file
errors = validate_excel_file(Path("input.xlsx"))
if not errors:
    # Process
    output = process_single_excel(
        Path("input.xlsx"),
        Path("results/"),
        verbose=True
    )
```

## Modern Python Packaging Standards

This package follows:

- **PEP 517**: Build system independence
- **PEP 518**: pyproject.toml specification
- **PEP 621**: Project metadata in pyproject.toml
- **PEP 440**: Version identification
- **src/ layout**: Package discovery best practice
- **Type hints**: Throughout codebase (Python 3.10+)
- **Black formatting**: Consistent code style
- **Ruff linting**: Fast, comprehensive checking

## Advantages of This Structure

1. **Modern**: Uses latest Python packaging standards
2. **Minimal**: pyproject.toml only, no setup.cfg needed
3. **Type-safe**: Type hints for better IDE support
4. **Discoverable**: Clear package structure
5. **Testable**: Proper separation of source and tests
6. **Maintainable**: Good documentation and changelog
7. **Professional**: Follows industry best practices
8. **Fast builds**: hatchling is much faster than setuptools

## Migration Notes

If upgrading from old setup.py-only approach:

- Old: setup.py with all configuration
- New: pyproject.toml with minimal setup.py for compatibility
- Version: Now in `__init__.py`, not setup.py
- Scripts: Defined in pyproject.toml [project.scripts]
- Dependencies: In pyproject.toml [project.dependencies]

## Additional Resources

- **Build backend**: https://hatch.pypa.io/
- **Packaging guide**: https://packaging.python.org/
- **PEP 621**: https://peps.python.org/pep-0621/
- **Semantic Versioning**: https://semver.org/
