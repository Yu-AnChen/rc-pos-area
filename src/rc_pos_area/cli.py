#!/usr/bin/env python3
"""
Image Analysis CLI Tool for Microscopy Data Processing

This tool provides three modes:
1. Single file processing
2. Batch processing of multiple files
3. Report generation from processed files
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import shutil
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import matplotlib.pyplot as plt

# Import processing functions
from rc_pos_area.processor import (
    validate_excel_file,
    process_single_excel,
    ValidationError
)
from rc_pos_area.report import generate_summary_report


def setup_argparse() -> argparse.ArgumentParser:
    """Setup command-line argument parser."""
    parser = argparse.ArgumentParser(
        description='CLI Tool for Positive Area Calculation',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global options
    parser.add_argument('--verbose', action='store_true', help='Detailed progress output')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')
    
    subparsers = parser.add_subparsers(dest='mode', help='Processing mode', required=True)
    
    # Mode 1: Single file processing
    single_parser = subparsers.add_parser('single', help='Process a single Excel file')
    single_parser.add_argument('input_excel', type=str, help='Input Excel file path')
    single_parser.add_argument('--output-dir', type=str, default='results',
                              help='Output directory (default: results/)')
    
    # Mode 2: Batch processing
    batch_parser = subparsers.add_parser('batch', help='Process multiple Excel files')
    batch_parser.add_argument('input_dir', type=str, help='Input directory containing Excel files')
    batch_parser.add_argument('--output-dir', type=str, default='results',
                             help='Output directory (default: results/)')
    batch_parser.add_argument('--dry-run', action='store_true',
                             help='Validate only, do not process')
    
    # Mode 3: Report generation
    report_parser = subparsers.add_parser('report', help='Generate summary report')
    report_parser.add_argument('processed_dir', type=str,
                              help='Directory containing processed Excel files')
    report_parser.add_argument('--output', type=str, default=None,
                              help='Output filename (default: Summary-{timestamp}.xlsx)')
    
    return parser


def find_excel_files(directory: str) -> List[Path]:
    """Find all Excel files in a directory."""
    dir_path = Path(directory)
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    excel_files = list(dir_path.glob('*.xlsx'))
    # Filter out processed files and temporary Excel files
    excel_files = [f for f in excel_files 
                   if not f.name.startswith('~$') 
                   and not f.name.endswith('_processed.xlsx')]
    
    return sorted(excel_files)


def validate_batch(excel_files: List[Path], verbose: bool = False) -> Tuple[bool, Dict]:
    """
    Validate all Excel files before processing.
    
    Returns:
        Tuple of (all_valid, validation_results)
    """
    validation_results = {}
    all_valid = True
    
    print(f"\n{'='*60}")
    print(f"PRE-FLIGHT VALIDATION - Checking {len(excel_files)} file(s)")
    print(f"{'='*60}\n")
    
    for excel_file in excel_files:
        if verbose:
            print(f"Validating: {excel_file.name}")
        
        errors = validate_excel_file(excel_file)
        validation_results[excel_file] = errors
        
        if errors:
            all_valid = False
            print(f"\n❌ {excel_file.name}:")
            for error in errors:
                print(f"   - {error}")
        else:
            if verbose:
                print(f"✓ {excel_file.name}: OK")
    
    print(f"\n{'='*60}")
    if all_valid:
        print(f"✓ All {len(excel_files)} file(s) passed validation")
    else:
        failed_count = sum(1 for errors in validation_results.values() if errors)
        print(f"❌ {failed_count} file(s) failed validation")
        print("\nPlease fix the issues above before processing.")
        print("You can either:")
        print("  1. Fix the errors in the Excel files")
        print("  2. Remove problematic files from the input directory")
    print(f"{'='*60}\n")
    
    return all_valid, validation_results


def mode_single(args, verbose: bool, quiet: bool):
    """Process a single Excel file."""
    input_file = Path(args.input_excel)
    output_dir = Path(args.output_dir)
    
    if not input_file.exists():
        print(f"❌ Error: Input file not found: {input_file}")
        sys.exit(1)
    
    # Validate
    if not quiet:
        print(f"Validating {input_file.name}...")
    
    errors = validate_excel_file(input_file)
    if errors:
        print(f"❌ Validation failed:")
        for error in errors:
            print(f"   - {error}")
        sys.exit(1)
    
    if not quiet:
        print("✓ Validation passed")
    
    # Process
    try:
        output_file = process_single_excel(input_file, output_dir, verbose, quiet)
        if not quiet:
            print(f"\n✓ Successfully processed: {output_file.name}")
            print(f"   Output: {output_file}")
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def mode_batch(args, verbose: bool, quiet: bool):
    """Process multiple Excel files in batch."""
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    dry_run = args.dry_run
    
    # Find Excel files
    try:
        excel_files = find_excel_files(input_dir)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    if not excel_files:
        print(f"No Excel files found in {input_dir}")
        sys.exit(0)
    
    if not quiet:
        print(f"Found {len(excel_files)} Excel file(s) in {input_dir}")
    
    # Validate all files
    all_valid, validation_results = validate_batch(excel_files, verbose)
    
    if not all_valid:
        sys.exit(1)
    
    if dry_run:
        print("Dry run complete. No files were processed.")
        sys.exit(0)
    
    # Process all files
    print(f"\n{'='*60}")
    print(f"PROCESSING {len(excel_files)} FILE(S)")
    print(f"{'='*60}\n")
    
    successful = 0
    failed = 0
    
    for i, excel_file in enumerate(excel_files, 1):
        if not quiet:
            print(f"[{i}/{len(excel_files)}] Processing {excel_file.name}...")
        
        try:
            output_file = process_single_excel(excel_file, output_dir, verbose, quiet)
            successful += 1
            if not quiet:
                print(f"   ✓ Created: {output_file.name}")
        except Exception as e:
            failed += 1
            print(f"   ❌ Failed: {e}")
            if verbose:
                import traceback
                traceback.print_exc()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"BATCH PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")


def mode_report(args, verbose: bool, quiet: bool):
    """Generate summary report from processed files."""
    processed_dir = Path(args.processed_dir)
    
    if not processed_dir.exists():
        print(f"❌ Error: Directory not found: {processed_dir}")
        sys.exit(1)
    
    # Find processed Excel files
    processed_files = list(processed_dir.glob('*_processed.xlsx'))
    
    if not processed_files:
        print(f"No processed files (*_processed.xlsx) found in {processed_dir}")
        sys.exit(0)
    
    if not quiet:
        print(f"Found {len(processed_files)} processed file(s)")
    
    # Generate output filename
    if args.output:
        output_file = Path(args.output)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = processed_dir / f'Summary-{timestamp}.xlsx'
    
    # Generate report
    try:
        generate_summary_report(processed_files, output_file, verbose, quiet)
        if not quiet:
            print(f"\n✓ Summary report created: {output_file}")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    parser = setup_argparse()
    args = parser.parse_args()
    
    # Handle verbose/quiet flags
    verbose = args.verbose
    quiet = args.quiet
    
    if verbose and quiet:
        print("Error: Cannot use both --verbose and --quiet")
        sys.exit(1)
    
    # Route to appropriate mode
    if args.mode == 'single':
        mode_single(args, verbose, quiet)
    elif args.mode == 'batch':
        mode_batch(args, verbose, quiet)
    elif args.mode == 'report':
        mode_report(args, verbose, quiet)


if __name__ == '__main__':
    main()
