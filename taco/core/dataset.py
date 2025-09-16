import sys
from typing import List

from datasets import load_dataset


def load_taco_dataset(difficulties: List[str], skills: List[str]):
    """
    Load TACO dataset in this way to bypass deprecated error from TACO.py in HF datasets
    """
    print(f"Loading TACO dataset with difficulties={difficulties}, skills={skills}")

    try:
        print("Loading TACO dataset from Arrow files...")
        # Load test split directly from Arrow file (1000 problems)
        taco = load_dataset(
            "arrow",
            data_files="hf://datasets/BAAI/TACO/test/data-00000-of-00001.arrow"
        )['train']

        # Apply filtering if needed
        if difficulties != ["ALL"]:
            print(f"Filtering by difficulties: {difficulties}")
            taco = taco.filter(lambda x: x['difficulty'] in difficulties)

        if skills != ["ALL"]:
            print(f"Filtering by skills: {skills}")
            # Skills are stored as string representation of list, need to evaluate
            taco = taco.filter(
                lambda x: any(skill in eval(x['skill_types']) for skill in skills)
            )

        print(f"Loaded {len(taco)} problems")
        return taco

    except Exception as e:
        print(f"Error loading TACO dataset: {e}")
        sys.exit(1)


def parse_filters(difficulties_str: str, skills_str: str) -> tuple[List[str], List[str]]:
    """Parse comma-separated difficulty and skill filters"""
    if difficulties_str == "ALL":
        difficulties = ["ALL"]
    else:
        difficulties = [d.strip() for d in difficulties_str.split(",")]

    if skills_str == "ALL":
        skills = ["ALL"]
    else:
        skills = [s.strip() for s in skills_str.split(",")]

    return difficulties, skills
