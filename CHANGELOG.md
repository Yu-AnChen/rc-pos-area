# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-10

### Added
- Initial release of rc-pos-area package
- Three-mode CLI interface (single, batch, report)
- Comprehensive pre-flight validation for batch processing
- Tissue region calculation using channel 2 as mask
- Automatic grouping and color-coding in summary reports
- Support for 1-based channel indexing in Excel files
- Gaussian filtering with configurable sigma
- Metrics calculation for entire image and tissue region:
  - Total area and positive area
  - Positive fraction percentages
  - Tissue-specific area and fractions
- Tab10 color palette for visual group distinction
- Dry-run mode for validation without processing
- Verbose and quiet output modes
- Professional Excel output with auto-sized columns

### Features
- **Single file processing**: Process one Excel file at a time
- **Batch processing**: Process multiple files with pre-flight validation
- **Report generation**: Create grouped, color-coded summary reports
- **Validation checks**:
  - Excel file format and required sheets
  - Channel 2 presence (required for tissue mask)
  - Image file existence and readability
  - Channel number validity (1-based indexing)
  - palom.reader.OmePyramidReader compatibility
  - Output directory write permissions

### Technical Details
- Python >=3.10 support
- Modern packaging with pyproject.toml and hatchling
- Dynamic versioning from __init__.py
- Modular architecture (cli, processor, report modules)
- Type hints throughout codebase
- Comprehensive error handling and user feedback

### Dependencies
- pandas >=2.0.0
- openpyxl >=3.1.0
- numpy >=1.24.0
- dask-image >=2023.0.0
- palom >=2023.0.0
- matplotlib >=3.7.0

[0.1.0]: https://github.com/yu-anchen/rc-pos-area/releases/tag/v0.1.0
