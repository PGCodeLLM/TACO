import json
from typing import Any, Dict


def format_taco_prompt(sample: Dict[str, Any]) -> str:
    """
    Format TACO sample into prompt following original TACO format
    """
    question = sample.get("question", "")
    starter_code = sample.get("starter_code", "")
    input_output = sample.get("input_output", "")

    # Build prompt following original TACO format
    prompt = "\nQUESTION:\n"
    prompt += question

    # Handle starter code
    starter_code = None if len(starter_code) == 0 else starter_code

    # Parse input_output to get function name
    try:
        input_output_data = json.loads(input_output)
        fn_name = None if not input_output_data.get("fn_name") else input_output_data["fn_name"]
    except (ValueError, json.JSONDecodeError):
        fn_name = None

    # Add starter code if present
    if starter_code:
        prompt += starter_code

    # Add format specification (important for TACO evaluation)
    if (not fn_name) and (not starter_code):
        call_format = "\nUse Standard Input format"
        prompt += call_format
    else:
        call_format = "\nUse Call-Based format"
        prompt += call_format

    prompt += "\nANSWER:\n"

    return prompt
