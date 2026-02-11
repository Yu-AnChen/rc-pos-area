"""
Image Analysis Tool - CLI for processing microscopy image analysis data.

This package provides a command-line tool for batch processing of microscopy
images with automated tissue region detection and metric calculation.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("image-analysis-tool")
except PackageNotFoundError:
    # package is not installed
    pass

from image_analysis_tool.processor import process_single_excel, validate_excel_file
from image_analysis_tool.report import generate_summary_report

__all__ = [
    "process_single_excel",
    "validate_excel_file",
    "generate_summary_report",
    "__version__",
]
