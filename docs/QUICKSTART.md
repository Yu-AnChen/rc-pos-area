# Quick Start Guide

Get started with rc-pos-area in 5 minutes!

## 1. Install

```bash
pip install rc-pos-area
```

## 2. Verify Installation

```bash
image-analysis --help
```

## 3. Prepare Your Data

Create an Excel file with two sheets:

### Files Sheet
| Slide Name | File Path |
|------------|-----------|
| MySample | /path/to/image.ome.tif |

### Thresholds Sheet
| Channel # | Antibody | Threshold |
|-----------|----------|-----------|
| 2 | DAPI | 500 |
| 3 | CD3 | 1300 |
| 5 | CD8 | 1650 |

**Important**: Channel 2 is required (defines tissue region)

## 4. Process a Single File

```bash
image-analysis single my_experiment.xlsx
```

Output: `results/my_experiment_processed.xlsx`

## 5. Process Multiple Files

```bash
# Validate first (dry-run)
image-analysis batch /path/to/excel/files --dry-run

# Process all files
image-analysis batch /path/to/excel/files
```

## 6. Generate Summary Report

```bash
image-analysis report results/
```

Output: `results/Summary-{timestamp}.xlsx`

## Common Workflows

### Complete Analysis Pipeline

```bash
# Step 1: Batch process
image-analysis batch ./experiments/ --output-dir ./results/

# Step 2: Generate report
image-analysis report ./results/

# Done! Check results/Summary-*.xlsx
```

### With Custom Options

```bash
# Verbose output
image-analysis batch ./data/ --verbose

# Custom output directory
image-analysis single sample.xlsx --output-dir ./processed/

# Quiet mode (minimal output)
image-analysis batch ./data/ --quiet
```

### Validation Only

```bash
# Check files without processing
image-analysis batch ./data/ --dry-run
```

## Output Explained

### Processed Files

Each input file becomes `{name}_processed.xlsx` with metrics:

- **Area (µm²)** - Total image area
- **Positive Area (µm²)** - Area above threshold
- **Positive Fraction (%)** - Percentage positive
- **Tissue Area (µm²)** - Channel 2 positive area
- **Positive Area in Tissue (µm²)** - Positive within tissue
- **Positive Fraction in Tissue (%)** - Percentage in tissue

### Summary Report

Groups files by channel configuration with:
- Summary sheet listing all files
- Individual sheets per slide
- Color-coded by group
- Alphabetically sorted within groups

## Troubleshooting

### File Not Found

```
❌ Error: Image file does not exist
```
→ Check File Path in your Excel Files sheet

### Missing Channel 2

```
❌ Error: Channel #2 is required
```
→ Add Channel 2 to your Thresholds sheet

### Invalid Channel Number

```
❌ Error: Channel # 15 is invalid (image has 10 channels: 1-10)
```
→ Channel numbers must exist in image (1-based)

## Next Steps

- Read full [README.md](../README.md) for detailed documentation
- Check [QUICKREF.md](QUICKREF.md) for command reference
- See [Examples](../examples/) for sample data (if available)

## Getting Help

```bash
# Help for specific command
image-analysis single --help
image-analysis batch --help
image-analysis report --help
```

Need more help? Check the [documentation](../README.md) or open an issue on GitHub.
