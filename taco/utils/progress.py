import json
from datetime import datetime
from pathlib import Path


def init_progress(total_problems: int, output_dir: Path):
    """Create progress.json file"""
    progress = {
        "completed_problems": 0,
        "total_problems": total_problems,
        "current_problem": 0,
        "last_updated": datetime.now()
    }

    with open(output_dir / "progress.json", "w") as f:
        json.dump(progress, f, indent=2)


def update_progress(output_dir: Path, current_problem: int = None, completed_problems: int = None):
    """Update progress.json file"""
    progress_file = output_dir / "progress.json"

    # Read existing progress
    if progress_file.exists():
        with open(progress_file, "r") as f:
            progress = json.load(f)
    else:
        progress = {"completed_problems": 0, "total_problems": 0, "current_problem": 0}

    # Update fields if provided
    if current_problem is not None:
        progress["current_problem"] = current_problem
    if completed_problems is not None:
        progress["completed_problems"] = completed_problems

    progress["last_updated"] = datetime.now()

    # Write back
    with open(progress_file, "w") as f:
        json.dump(progress, f, indent=2)
