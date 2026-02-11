# Tissue Region Feature - Changelog

## Feature Added: Tissue Region Metrics

### Overview
Added calculation of channel positivity within a tissue region, defined by channel 2 positivity. All channels now report metrics both for the entire image and within the tissue region.

## Changes Made

### 1. `image_processor.py` - Validation

**Added channel 2 requirement check:**
```python
# Check that channel 2 exists (required for tissue region mask)
if 2 not in thresholds_df['Channel #'].values:
    errors.append("Channel #2 is required for tissue region definition but not found in 'Thresholds' sheet")
    return errors
```

This check is performed during pre-flight validation before any processing begins.

### 2. `image_processor.py` - Processing

**Added tissue mask creation:**
```python
# First, create tissue region mask from channel 2
channel_2_threshold = thresholds_df.loc[2, 'Threshold']
channel_2_idx = 2 - 1  # Convert to 0-based
tissue_img = reader.pyramid[PYRAMID_LEVEL][channel_2_idx].astype('float32')
tissue_gimg = dask_image.ndfilters.gaussian_filter(tissue_img, GAUSSIAN_SIGMA)
tissue_mask = tissue_gimg > channel_2_threshold
tissue_area = int(np.sum(tissue_mask)) * PIXEL_SIZE**2
```

**Added tissue-specific metrics for each channel:**
```python
# Tissue region metrics
thresholds_df.loc[cc, 'Tissue Area (µm^2)'] = tissue_area
positive_in_tissue = np.sum((gimg > tt) & tissue_mask)
thresholds_df.loc[cc, 'Positive Area in Tissue (µm^2)'] = int(positive_in_tissue) * PIXEL_SIZE**2
```

**Added tissue fraction calculation:**
```python
thresholds_df['Positive Fraction in Tissue (%)'] = 100 * (
    thresholds_df['Positive Area in Tissue (µm^2)'] / thresholds_df['Tissue Area (µm^2)']
)
```

### 3. Documentation Updates

**Updated files:**
- `README.md` - Added tissue region description and new column documentation
- `IMPLEMENTATION_SUMMARY.md` - Added tissue region calculation section
- `QUICKREF.md` - (if needed) Update with tissue region notes

## New Output Columns

The processed Excel files now contain these columns (in order):

1. Channel #
2. Antibody
3. ArgoFluor
4. Threshold
5. **Area (µm^2)** - Total image area
6. **Positive Area (µm^2)** - Positive area in entire image
7. **Positive Fraction (%)** - Positive fraction in entire image
8. **Tissue Area (µm^2)** - Area of tissue region (same for all channels)
9. **Positive Area in Tissue (µm^2)** - Positive area within tissue region
10. **Positive Fraction in Tissue (%)** - Positive fraction within tissue region

## Behavior Notes

### Channel 2 (Tissue Mask)
- For channel 2 itself:
  - `Tissue Area (µm^2)` = `Positive Area (µm^2)` (by definition)
  - `Positive Area in Tissue (µm^2)` = `Positive Area (µm^2)` (by definition)
  - `Positive Fraction in Tissue (%)` = 100.00000% (always)

### Other Channels
- Tissue region is the same for all channels (defined by channel 2)
- `Tissue Area (µm^2)` is identical for all channels
- `Positive Area in Tissue (µm^2)` varies per channel based on that channel's threshold
- This allows comparison of marker expression specifically within tissue regions

## Algorithm

1. **Load image** and all channel thresholds from Excel
2. **Create tissue mask** (done once per image):
   - Load channel 2 at pyramid level 2
   - Apply Gaussian filter (σ=1)
   - Create binary mask: `tissue_mask = filtered_channel_2 > threshold_2`
   - Calculate tissue area
3. **Process each channel** (including channel 2):
   - Load channel at pyramid level 2
   - Apply Gaussian filter (σ=1)
   - Calculate overall metrics (entire image)
   - Calculate tissue-specific metrics using tissue mask
4. **Calculate fractions** for both overall and tissue-specific metrics
5. **Write results** to Excel

## Example Output

For a file with channels 2, 3, 5:

| Channel # | Threshold | Area (µm^2) | Positive Area (µm^2) | Positive Fraction (%) | Tissue Area (µm^2) | Positive Area in Tissue (µm^2) | Positive Fraction in Tissue (%) |
|-----------|-----------|-------------|----------------------|-----------------------|--------------------|---------------------------------|----------------------------------|
| 2 | 500 | 1234567.89 | 234567.89 | 19.01234 | 234567.89 | 234567.89 | 100.00000 |
| 3 | 1300 | 1234567.89 | 123456.78 | 10.00000 | 234567.89 | 98765.43 | 42.10000 |
| 5 | 1650 | 1234567.89 | 87654.32 | 7.10000 | 234567.89 | 65432.10 | 27.89000 |

Note how:
- Channel 2 has 100% positive fraction in tissue (by definition)
- All channels share the same tissue area (234567.89 µm^2)
- Tissue fractions can be higher or lower than overall fractions depending on marker distribution

## Validation

New validation check added:
- ✓ Channel 2 must be present in Thresholds sheet
- Error message: "Channel #2 is required for tissue region definition but not found in 'Thresholds' sheet"
- Check occurs during pre-flight validation (before any processing)

## Backward Compatibility

**Breaking Change**: Files without channel 2 will now fail validation and cannot be processed.

**Migration**: Ensure all input Excel files include channel 2 in the Thresholds sheet with an appropriate threshold value.

## Testing Recommendations

1. Verify channel 2 always shows 100% positive fraction in tissue
2. Check that tissue area is the same for all channels in a file
3. Verify tissue-specific metrics are ≤ overall metrics
4. Test with images where tissue is a small portion of total area
5. Test validation with files missing channel 2
