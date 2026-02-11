# rc-pos-area: Positive Area Calculator

> Calculate positive area per channel in multiplex whole slide images using user-defined intensity thresholds.

## What Does This Tool Do?

For each channel listed in your input, this tool calculates what fraction of the image (and of a tissue region) is above the threshold you set. Specifically it:

- Applies a threshold to each channel and measures the **positive area** in the whole image and within a **tissue region** defined by channel 2
- Processes **single files or entire folders** in batch with pre-flight validation
- Produces a **summary report** grouping samples by channel configuration with color-coding

---

## Before You Start

### What You'll Need

1. **Your microscopy images** in OME-TIFF format
2. **An Excel file** for each image with:
   - Your sample information (slide name, file path)
   - Channel thresholds you want to use

---

## Installation

We use **pixi** to set up everything automatically. Pixi is a package manager that creates an isolated environment with all the required software — think of it as a self-contained bubble for this tool.

### Step 1: Install pixi

Open **PowerShell** (search for "PowerShell" in the Start menu) and run:

```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

Or download the installer from [pixi.sh](https://pixi.prefix.dev/latest/installation/#__tabbed_1_2).

<details>
<summary><b>Mac / Linux</b></summary>

Open Terminal and run:

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

</details>

### Step 2: Set Up the Environment

Run these commands in PowerShell:

```powershell
# Create and enter a new folder
mkdir rc-pos-area-env
cd rc-pos-area-env

# Download configuration files
curl -OL https://raw.githubusercontent.com/Yu-AnChen/rc-pos-area/refs/heads/main/pixi/pixi.toml
curl -OL https://raw.githubusercontent.com/Yu-AnChen/rc-pos-area/refs/heads/main/pixi/pixi.lock

# Install everything
pixi install
```

**This may take a few minutes** the first time as it downloads Python and all required libraries.

<details>
<summary><b>Mac / Linux</b></summary>

```bash
mkdir rc-pos-area-env && cd rc-pos-area-env

curl -OL https://raw.githubusercontent.com/Yu-AnChen/rc-pos-area/refs/heads/main/pixi/pixi.toml
curl -OL https://raw.githubusercontent.com/Yu-AnChen/rc-pos-area/refs/heads/main/pixi/pixi.lock

pixi install
```

</details>

### Step 3: Verify Installation

```powershell
pixi run pos-area --help
```

You should see a help message listing available commands.

---

## Preparing Your Input Files

Create an Excel file (`.xlsx`) for each image with **two sheets**:

### Sheet 1: "Files"

| Slide Name | File Path |
|------------|-----------|
| Sample_001 | C:\Images\Sample_001.ome.tif |

- **Slide Name**: A name for your sample (used in reports)
- **File Path**: Full path to your OME-TIFF image file

### Sheet 2: "Thresholds"

| Channel # | Antibody | ArgoFluor | Threshold |
|-----------|----------|-----------|-----------|
| 2 | DAPI | Argo550 | 500 |
| 3 | CD3 | Argo660 | 1300 |
| 5 | CD8 | Argo690 | 1650 |

- **Channel #**: Channel number (starts at 1, not 0!)
- **Antibody**: Marker name (optional, for your reference)
- **ArgoFluor**: Fluorophore name (optional, for your reference)
- **Threshold**: Intensity cutoff for positive signal

**Important:** Channel 2 is required — it defines the tissue region for analysis.

---

## Using the GUI (Recommended)

The graphical interface is the easiest way to use this tool — no command-line experience needed.

### Launching the GUI

```powershell
pixi run parea
```

A window will open with three tabs: **Single**, **Batch**, and **Report**.

### Single Tab — Process One File

Use this to analyze one sample at a time, or to test that your Excel file is set up correctly.

1. Click **Browse** next to "Input Excel" and select your `.xlsx` file
2. Click **Browse** next to "Output Dir" to choose where results are saved (default: `results`)
3. Click **Validate** to check your file for errors without processing
4. Click **Process** to run the analysis

The result will be a `*_processed.xlsx` file in your output folder.

### Batch Tab — Process Multiple Files

Use this when you have many samples to analyze at once.

1. Click **Browse** next to "Input Dir" and select the folder containing your `.xlsx` files
2. Click **Browse** next to "Output Dir" to choose where results are saved
3. (Optional) Check **Dry run** to validate all files without processing them — useful for catching errors before a long run
4. Click **Run Batch**

The tool validates **all** files first. If any file has an error, it will tell you before processing anything, so you can fix issues first.

### Report Tab — Generate Summary Report

Use this after processing to combine all results into one report.

1. Click **Browse** next to "Processed Dir" and select the folder containing your `*_processed.xlsx` files
2. (Optional) Click **Browse** next to "Output File" to choose a file name. If left blank, a timestamped name is generated automatically.
3. Click **Generate Report**

The summary report contains:

- **Summary sheet**: All samples listed with group assignments, color-coded
- **Individual sheets**: One per sample with detailed metrics
- **Color-coded tabs**: Samples with the same channel configuration share a color

### Status Log

The log area at the bottom of the window shows progress and any errors. Use the **Clear Log** button to reset it.

---

## Using the Command Line

<details>
<summary><b>Expand for command-line usage</b></summary>

All commands follow this pattern:

```powershell
pixi run pos-area <mode> <input> [options]
```

### Process a Single File

```powershell
pixi run pos-area single my_sample.xlsx
pixi run pos-area single my_sample.xlsx --output-dir my_results
pixi run pos-area single my_sample.xlsx --verbose
```

### Process Multiple Files (Batch)

```powershell
pixi run pos-area batch my_excel_files\

# Validate only, don't process
pixi run pos-area batch my_excel_files\ --dry-run

# Minimal output
pixi run pos-area batch my_excel_files\ --quiet
```

### Generate Summary Report

```powershell
pixi run pos-area report results\
pixi run pos-area report results\ --output Experiment_Summary.xlsx
```

### Options

- `--verbose`: Show detailed progress
- `--quiet`: Minimal output (errors and final results only)
- `--output-dir <dir>`: Specify output directory (default: `results`)
- `--dry-run` (batch only): Validate files without processing

</details>

---

## Step-by-Step Workflow Example

You have 10 samples from an experiment. Each has an OME-TIFF image file and an Excel file with thresholds. All Excel files are in a folder called `experiment_data`.

### Using the GUI

1. Launch the GUI: `pixi run parea`
2. Go to the **Batch** tab
3. Set "Input Dir" to your `experiment_data` folder
4. Set "Output Dir" to `my_results`
5. Check **Dry run** and click **Run Batch** — fix any errors reported in the log
6. Uncheck **Dry run** and click **Run Batch** to process all files
7. Go to the **Report** tab
8. Set "Processed Dir" to `my_results`
9. Click **Generate Report**
10. Open the summary Excel file in your `my_results` folder

<details>
<summary><b>Using the command line</b></summary>

```powershell
# 1. Validate all files
pixi run pos-area batch experiment_data\ --dry-run

# 2. Process all samples
pixi run pos-area batch experiment_data\ --output-dir my_results

# 3. Generate summary report
pixi run pos-area report my_results\ --output Experiment_Summary.xlsx
```

</details>

---

## Understanding the Output

### Processed File Columns

Each processed file includes these calculations:

| Column | What It Means |
|--------|---------------|
| **Area (µm²)** | Total area of the entire image |
| **Positive Area (µm²)** | Area where signal is above threshold (whole image) |
| **Positive Fraction (%)** | Percentage of image that's positive |
| **Tissue Area (µm²)** | Area of the tissue region (from channel 2) |
| **Positive Area in Tissue (µm²)** | Positive area only within tissue |
| **Positive Fraction in Tissue (%)** | Percentage of tissue that's positive |

**Why two sets of metrics?**

- **Whole image metrics** include everything (tissue + background)
- **Tissue metrics** focus only on the tissue region defined by channel 2

This gives you more accurate quantification by excluding background areas.

---

## Troubleshooting

<details>
<summary><b>"Command not found: pixi"</b></summary>

Pixi isn't installed or not in your system PATH.

1. Reinstall pixi following the installation instructions above
2. Close and reopen PowerShell
3. If still not working, try restarting your computer

</details>

<details>
<summary><b>"Missing channel 2 in Thresholds sheet"</b></summary>

Your Excel file doesn't have channel 2. Channel 2 is required for tissue region definition. Add a row for channel 2 with an appropriate threshold (typically DAPI or another nuclear marker).

</details>

<details>
<summary><b>"Image file does not exist"</b></summary>

The file path in your Excel "Files" sheet is incorrect.

1. Open your Excel file
2. Check the "File Path" column in the "Files" sheet
3. Make sure the path is correct and the file exists
4. Use full paths (e.g., `C:\Images\sample.ome.tif` not `sample.ome.tif`)

</details>

<details>
<summary><b>"Invalid channel number"</b></summary>

You specified a channel number that doesn't exist in your image.

1. Check how many channels your image has
2. Make sure all channel numbers in your Thresholds sheet are ≤ the number of channels
3. Remember: channel numbers start at 1, not 0

</details>

<details>
<summary><b>Processing takes a long time</b></summary>

This is normal for large images. Processing time depends on image size. For large batches, consider processing files in smaller groups or running overnight.

</details>

### Still Having Issues?

Open an issue on [GitHub](https://github.com/Yu-AnChen/rc-pos-area/issues) with:

- What you did (the button you clicked or command you ran)
- The error message from the status log
- Your Excel file structure (without sensitive data)

---

## Tips

- **Test with one file first** using the Single tab to make sure your Excel format is correct
- **Use Dry run** in the Batch tab to validate before a long processing run
- **Use descriptive slide names** — "Sample_001" is better than "1"
- **Keep organized** — use separate folders for different experiments
- **Save your Excel templates** — reuse for similar experiments

---

## Additional Resources

- **Detailed Documentation**: See the [docs/](docs/) folder for technical details
- **Issues & Questions**: [GitHub Issues](https://github.com/Yu-AnChen/rc-pos-area/issues)
- **License**: MIT (see [LICENSE](LICENSE))