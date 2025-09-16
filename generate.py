#!/usr/bin/env python3
"""
TACO Evaluation with vLLM integration - Clean modular implementation

This is the main entry point for TACO evaluation. It uses the modular
taco package for clean separation of concerns.
"""

from taco.cli import parse_arguments, run_evaluation


def main():
    """Main evaluation function using modular components"""
    args = parse_arguments()
    run_evaluation(args)


if __name__ == "__main__":
    main()