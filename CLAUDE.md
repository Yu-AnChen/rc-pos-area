# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

rc-pos-area is a Python CLI tool for computing positive area in multi-channel whole slide images (WSI) based on user-provided intensity thresholds. It reads OME-TIFF microscopy images via palom, applies Gaussian filtering, and calculates area metrics both for the full image and within a tissue region defined by channel 2 positivity.

## Commands

### Development Setup
```bash
pip install -e ".[dev]"
```

### Running the CLI
```bash
pos-area single input.xlsx --output-dir results/
pos-area batch /path/to/excels --output-dir results/ [--dry-run]
pos-area report results/ --output MyReport.xlsx
```

### Code Quality
```bash
black src/                  # Format (line length: 100)
ruff check src/             # Lint
ruff check --fix src/       # Lint with auto-fix
```

### Testing
```bash
pytest                      # Run all tests
pytest -v                   # Verbose
```

## Architecture

The package lives in `src/rc_pos_area/` with three modules forming a pipeline:

- **`cli.py`** — Entry point (`pos-area` command → `rc_pos_area.cli:main`). Argparse-based with three subcommands: `single`, `batch`, `report`. Handles file discovery, pre-flight batch validation, and orchestration.
- **`processor.py`** — Core image processing. `validate_excel_file()` performs a 9-step validation chain. `process_single_excel()` opens images with `palom.reader.OmePyramidReader`, builds a tissue mask from channel 2, applies `dask_image.ndfilters.gaussian_filter` (sigma=1) at pyramid level 2, then computes area metrics per channel.
- **`report.py`** — Summary report generation. `assign_groups()` groups processed files by channel configuration (which channels are present). `generate_summary_report()` produces a multi-sheet Excel workbook with color-coded tabs (matplotlib Tab10 palette).

### Data Flow
```
Input .xlsx (Files sheet + Thresholds sheet)
  → validate_excel_file() checks format, image accessibility, channel validity
  → process_single_excel() reads image, computes per-channel metrics
  → outputs *_processed.xlsx with 6 new metric columns
  → generate_summary_report() combines processed files into grouped summary workbook
```

### Key Constants (processor.py)
- `PYRAMID_LEVEL = 2`
- `GAUSSIAN_SIGMA = 1`
- Pixel size: `0.325 * 2^PYRAMID_LEVEL` microns

### Channel Indexing
Excel files use 1-based channel numbers (user-facing). The processor converts to 0-based indexing when accessing image arrays. Channel 2 (1-based) is always required as it defines the tissue region mask.

## Build System

- **setuptools** with `pyproject.toml`, version from git tags via **setuptools_scm**
- **pixi** environment config in `pixi/` (targets win-64, conda-forge channel)
