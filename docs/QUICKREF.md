# Quick Reference Guide

## Commands at a Glance

### Process Single File
```bash
python image_analysis_cli.py single <input.xlsx>
```

### Process All Files in Directory
```bash
python image_analysis_cli.py batch <directory>
```

### Generate Summary Report
```bash
python image_analysis_cli.py report <results_directory>
```

## Common Options

| Option | Description |
|--------|-------------|
| `--output-dir <dir>` | Specify output directory (default: results/) |
| `--dry-run` | Validate only, don't process (batch mode only) |
| `--verbose` | Show detailed progress |
| `--quiet` | Show minimal output |
| `--output <file>` | Specify report filename (report mode only) |

## Quick Workflows

### Basic Workflow
```bash
# 1. Process files
python image_analysis_cli.py batch ./data/

# 2. Generate report
python image_analysis_cli.py report results/
```

### Check Before Processing
```bash
# 1. Dry run to validate
python image_analysis_cli.py batch ./data/ --dry-run

# 2. If valid, process
python image_analysis_cli.py batch ./data/
```

### Custom Directories
```bash
# Process with custom output
python image_analysis_cli.py batch ./data/ --output-dir ./processed/

# Generate report with custom filename
python image_analysis_cli.py report ./processed/ --output MyReport.xlsx
```

## File Requirements

### Input Excel Files Must Have:
- **Files** sheet with columns: `Slide Name`, `File Path`
- **Thresholds** sheet with columns: `Channel #`, `Threshold` (and optional metadata)
- Exactly one row in Files sheet
- Valid channel numbers (must exist in image)
- Accessible image file

### Output Structure
```
results/
├── F8288_processed.xlsx
├── F8289_processed.xlsx
└── Summary-20260210_143022.xlsx
```

## Troubleshooting

### Validation Failed?
1. Check error messages for specific issues
2. Verify Excel file format matches requirements
3. Ensure image files exist at specified paths
4. Check channel numbers are valid (0-indexed)

### Permission Denied?
- Ensure output directory is writable
- Check file permissions on input files

### Module Not Found?
```bash
pip install pandas openpyxl numpy dask-image palom matplotlib
```

## Tips

✓ Use `--dry-run` to check files before processing  
✓ Use `--verbose` to debug issues  
✓ Process files are named `{original}_processed.xlsx`  
✓ Summary reports group by channel configuration  
✓ Sheet tabs are color-coded by group  
