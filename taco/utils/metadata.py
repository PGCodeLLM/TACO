import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


def create_metadata(args, difficulties: List[str], skills: List[str], total_tasks: int, output_dir: Path) -> Dict:
    """Create experiment metadata from args and save to file"""
    metadata = {
        "created_at": datetime.now().isoformat(),
        "experiment_id": args.experiment_id,
        "total_tasks": total_tasks,
        "model_name": args.model_name,
        "base_url": args.base_url,
        "difficulties": difficulties,
        "skills": skills,
        "n_samples": args.n_samples,
        "max_workers": args.max_workers,
        "parameters": {
            "temperature": args.temperature,
            "top_p": args.top_p,
            "top_k": args.top_k,
            "max_tokens": args.max_tokens,
            "presence_penalty": args.presence_penalty,
            "repetition_penalty": args.repetition_penalty,
        }
    }

    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    return metadata
