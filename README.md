# `rc-pos-area` CLI Tool

A command-line tool for calculating and summarizing positive area in image channels of a multiplex whole slide scan based on the thresholds provided by the user.

## Installation

### Using [pixi](https://pixi.prefix.dev/) (recommended)

1. [Install pixi](https://pixi.prefix.dev/latest/installation/#__tabbed_1_2)
2. Run the following command in command prompt or terminal:

    ```bash
    mkdir rc-pos-area-env && cd rc-pos-area-env

    curl -OL https://raw.githubusercontent.com/Yu-AnChen/rc-pos-area/refs/heads/main/pixi/pixi.toml
    curl -OL https://raw.githubusercontent.com/Yu-AnChen/rc-pos-area/refs/heads/main/pixi/pixi.lock
    
    pixi install
    ```

3. To run the tool, use `pixi run`:

    ```bash
    pixi run pos-area --help
    ```

## Requirements

- Python 3.10 or higher
- Dependencies (installed automatically):
  - pandas>=2.0.0
  - openpyxl>=3.1.0
  - numpy>=1.24.0
  - dask-image>=2023.0.0
  - palom>=2023.0.0
  - matplotlib>=3.7.0

## Usage

> [!NOTE]
> **Note:** If you installed using `pixi`, prefix the commands with `pixi run`.
> For example: `pixi run pos-area --help`.

Once installed, the tool is available as the `pos-area` command.

### Mode 1: Single File Processing

Process a single Excel file:

```bash
pos-area single <input_excel> [--output-dir <dir>]
```

**Examples:**
```bash
# Process F8288.xlsx, output to default 'results/' directory
pos-area single F8288.xlsx

# Process with custom output directory
pos-area single F8288.xlsx --output-dir /path/to/output

# Verbose output
pos-area single F8288.xlsx --verbose
```

**Output:** Creates `F8288_processed.xlsx` in the output directory.

### Mode 2: Batch Processing

Process all Excel files in a directory:

```bash
pos-area batch <input_dir> [--output-dir <dir>] [--dry-run]
```

**Examples:**
```bash
# Process all .xlsx files in current directory
pos-area batch .

# Process files with custom output directory
pos-area batch /path/to/excel/files --output-dir processed_results

# Dry run - validate only, don't process
pos-area batch . --dry-run

# Quiet mode
pos-area batch . --quiet
```

**Validation:** Before processing, the tool validates all files and checks:
1. Excel file format is correct
2. Required sheets ('Files', 'Thresholds') exist
3. Channel 2 is present in Thresholds sheet (required for tissue region definition)
4. Image file exists and is accessible
5. Image can be opened with `palom.reader.OmePyramidReader`
6. Channel numbers in Thresholds sheet are valid (1-based indexing)
7. Output directory can be created and files can be written

If any file fails validation, the tool will report all issues and exit without processing any files.

**Output:** Creates `{filename}_processed.xlsx` for each input file.

### Mode 3: Report Generation

Generate a summary report from processed files:

```bash
pos-area report <processed_dir> [--output <filename>]
```

**Examples:**
```bash
# Generate report from processed files in results/
pos-area report results/

# Specify custom output filename
pos-area report results/ --output MyReport.xlsx

# Verbose output
pos-area report results/ --verbose
```

**Output:** Creates `Summary-{timestamp}.xlsx` (or custom filename) with:
- **Summary sheet**: Lists all files with group assignments and color coding
- **Individual slide sheets**: One sheet per slide, ordered by group and slide name
- **Sheet tab colors**: Color-coded by group for easy visual identification
- **Grouping**: Files are automatically grouped by channel configuration

### Global Options

- `--verbose`: Show detailed progress information
- `--quiet`: Minimal output (only errors and final results)
- `--output-dir <dir>`: Specify output directory (default: `results/`)

**Note:** `--verbose` and `--quiet` cannot be used together.

## Input File Format

### Excel File Structure

Each input Excel file must contain:

#### 1. Files Sheet
| Slide Name | File Path |
|------------|-----------|
| F8288 | /path/to/image.ome.tif |

- Must have exactly one row
- **Slide Name**: Identifier for the slide (used in reports)
- **File Path**: Path to the OME-TIFF image file

#### 2. Thresholds Sheet
| Channel # | Antibody | ArgoFluor | Threshold |
|-----------|----------|-----------|-----------|
| 2 | AF1 | NaN | 500 |
| 3 | SPP1 | Argo520 | 1300 |
| 5 | CD3e | Argo548 | 1650 |

- **Channel #**: Channel number in the image (1-indexed, e.g., 1 for first channel)
- **Antibody**: Antibody name (optional metadata)
- **ArgoFluor**: Fluorophore name (optional metadata)
- **Threshold**: Intensity threshold for positive area calculation

**Note**: Channel numbers use 1-based indexing (1, 2, 3, ...) as is standard in Excel, but are automatically converted to 0-based indexing when accessing the image.

## Output File Format

### Processed Files

Processed files (`*_processed.xlsx`) contain the original sheets plus updated Thresholds sheet:

| Channel # | Antibody | ArgoFluor | Threshold | Area (µm^2) | Positive Area (µm^2) | Positive Fraction (%) | Tissue Area (µm^2) | Positive Area in Tissue (µm^2) | Positive Fraction in Tissue (%) |
|-----------|----------|-----------|-----------|-------------|----------------------|-----------------------|--------------------|--------------------------------|----------------------------------|
| 2 | AF1 | NaN | 500 | 1234567.89 | 234567.89 | 19.01234 | 234567.89 | 234567.89 | 100.00000 |
| 3 | SPP1 | Argo520 | 1300 | 1234567.89 | 123456.78 | 10.00000 | 234567.89 | 98765.43 | 42.10000 |

New columns:
- **Area (µm^2)**: Total area analyzed (entire image)
- **Positive Area (µm^2)**: Area above threshold (entire image)
- **Positive Fraction (%)**: Percentage of positive area (entire image)
- **Tissue Area (µm^2)**: Area of tissue region (defined by channel 2 positivity)
- **Positive Area in Tissue (µm^2)**: Area above threshold within tissue region only
- **Positive Fraction in Tissue (%)**: Percentage of positive area within tissue region

**Note**: Channel 2 is used to define the tissue region mask. All channels (including channel 2 itself) report metrics both for the entire image and within the tissue region.

### Summary Report

The summary report (`Summary-{timestamp}.xlsx`) contains:

1. **Summary Sheet**:
   - Lists all processed files
   - Shows group assignments
   - Color-coded by group

2. **Individual Slide Sheets**:
   - One sheet per slide (named by slide name)
   - Contains Thresholds data with calculated metrics
   - Ordered by: Group → Alphabetically within group
   - Tab color matches group color

## Processing Details

### Image Analysis Parameters

- **Pyramid Level**: 2 (configurable in `image_processor.py`)
- **Gaussian Sigma**: 1.0 (for smoothing)
- **Pixel Size**: 0.325 × 2^pyramid_level µm

### Tissue Region Definition

- **Tissue Mask**: Defined by channel 2 positivity (pixels where channel 2 > threshold)
- The tissue mask is calculated once per image and applied to all channels
- All channels report metrics both for the entire image and within the tissue region
- Channel 2's "Positive Fraction in Tissue" will always be 100% (by definition)

### Grouping Logic

Files are grouped by their channel configuration (which channels are present):
- Group 1: Files with channels [2, 3, 5, 11, 12, 13, 14, 15, 17]
- Group 2: Files with channels [2, 13, 18]
- etc.

Groups are assigned distinct colors from the Tab10 color palette.

## Workflow Examples

### Complete Workflow

```bash
# 1. Process all files in a directory
pos-area batch /data/experiments/batch1/ --output-dir results/batch1/

# 2. Generate summary report
pos-area report results/batch1/

# Result: Summary-20260210_143022.xlsx with all results
```

### Iterative Processing

```bash
# 1. Dry run to check all files
pos-area batch /data/experiments/ --dry-run

# 2. Fix any issues reported
# ... edit Excel files ...

# 3. Process after validation passes
pos-area batch /data/experiments/

# 4. Process a single problematic file separately
pos-area single /data/experiments/problematic_file.xlsx --verbose
```

## Troubleshooting

### Common Validation Errors

1. **Missing sheet**: Add 'Files' and/or 'Thresholds' sheet to Excel file
2. **Missing channel 2**: Channel 2 is required for tissue region definition - add it to Thresholds sheet
3. **Image file not found**: Check File Path in Files sheet, ensure file exists
4. **Invalid channel number**: Channel numbers must be 1-based (1, 2, 3, ...) and exist in image
5. **Cannot read image**: Ensure image is a valid OME-TIFF file readable by palom

### Tips

- Use `--verbose` to see detailed progress and error messages
- Use `--dry-run` in batch mode to validate before processing
- Check that all image files are accessible from the machine running the tool
- Ensure sufficient disk space for output files
- For large batches, consider processing in smaller groups

## License

See individual script headers for licensing information.
