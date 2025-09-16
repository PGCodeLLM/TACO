"""
TACO Integration Package

This package provides a clean, modular implementation of TACO evaluation
using vLLM API for model inference.
"""

from .core.evaluator import TACOEvaluator
from .core.dataset import load_taco_dataset
from .core.prompt import format_taco_prompt
from .utils.progress import init_progress, update_progress
from .utils.metadata import create_metadata

__version__ = "1.0.0"
__all__ = [
    "TACOEvaluator",
    "load_taco_dataset",
    "format_taco_prompt",
    "init_progress",
    "update_progress",
    "create_metadata"
]