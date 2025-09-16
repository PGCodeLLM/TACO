"""
Command Line Interface for TACO evaluation
"""

from .args import parse_arguments
from .runner import run_evaluation

__all__ = ["parse_arguments", "run_evaluation"]