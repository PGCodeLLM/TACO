import json
import time
from pathlib import Path
from typing import Dict, List

from ..core.evaluator import TACOEvaluator
from ..core.dataset import load_taco_dataset, parse_filters
from ..core.prompt import format_taco_prompt
from ..utils.progress import init_progress, update_progress
from ..utils.metadata import create_metadata


def run_evaluation(args) -> None:
    """
    Run complete TACO evaluation with the given arguments

    Args:
        args: Parsed command line arguments
    """
    print("Starting TACO evaluation...")

    # Parse filters
    difficulties, skills = parse_filters(args.difficulties, args.skills)

    # Load dataset
    taco = load_taco_dataset(difficulties, skills)

    # Setup output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create experiment metadata
    metadata = create_metadata(args, difficulties, skills, len(taco), output_dir)

    # Initialize progress tracking
    init_progress(len(taco), output_dir)

    # Initialize evaluator
    evaluator = TACOEvaluator(
        base_url=args.base_url,
        model_name=args.model_name,
        api_key=args.api_key,
        temperature=args.temperature,
        top_p=args.top_p,
        top_k=args.top_k,
        max_completion_tokens=args.max_tokens,
        presence_penalty=args.presence_penalty,
        repetition_penalty=args.repetition_penalty,
        timeout=args.timeout,
    )

    # Run evaluation
    total_problems, total_time = process_problems(
        taco, evaluator, args, output_dir
    )

    # Final progress update
    update_progress(output_dir, completed_problems=total_problems)

    print("TACO evaluation finished successfully!")


def process_problems(taco, evaluator, args, output_dir: Path):
    """Process all TACO problems and generate solutions"""
    output = []
    output_file = output_dir / f"taco_results_{args.experiment_id}.json"
    total_problems = len(taco)

    print(f"Starting generation for {total_problems} problems with {args.n_samples} samples each")
    start_time = time.time()

    for idx, sample in enumerate(taco):
        problem_start = time.time()
        print(f"Processing problem {idx+1}/{total_problems}")

        # Update current problem in progress
        update_progress(output_dir, current_problem=idx + 1)

        # Format prompt and generate solutions
        prompt = format_taco_prompt(sample)
        generations = evaluator.generate_batch(prompt, args.n_samples, args.max_workers)

        # Store results
        results = {"task_id": idx, "prompt": prompt, "output": generations}
        output.append(results)

        problem_time = time.time() - problem_start
        print(f"Problem {idx+1} completed in {problem_time:.2f}s")

        # Update completed problems count
        update_progress(output_dir, completed_problems=idx + 1)

        # Save intermediate results every 10 problems
        if (idx + 1) % 10 == 0:
            save_results(output, output_file)
            print(f"Saved intermediate results to {output_file}")

    # Save final results
    save_results(output, output_file)

    total_time = time.time() - start_time
    print_completion_stats(total_time, total_problems, output_file)

    return total_problems, total_time


def save_results(output: List[Dict], output_file: Path):
    """Save results to JSON file"""
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)


def print_completion_stats(total_time: float, total_problems: int, output_file: Path):
    """Print completion statistics"""
    print(f"\nEvaluation completed!")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average time per problem: {total_time/total_problems:.2f}s")
    print(f"Results saved to: {output_file}")
