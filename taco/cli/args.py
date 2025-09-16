import argparse


def parse_arguments():
    """Parse command line arguments for TACO evaluation"""
    parser = argparse.ArgumentParser(
        description="TACO evaluation with vLLM using standard patterns"
    )

    # Required parameters
    parser.add_argument("--experiment_id", required=True, help="Experiment identifier")
    parser.add_argument(
        "--base_url",
        required=True,
        help="vLLM API base URL (e.g., http://host:port/v1)",
    )
    parser.add_argument("--model_name", required=True, help="Model name")
    parser.add_argument("--api_key", required=True, help="API key")
    parser.add_argument("--output_dir", required=True, help="Output directory")

    # Inference parameters (optional)
    parser.add_argument("--temperature", type=float, help="Temperature")
    parser.add_argument("--top_p", type=float, help="Top-p")
    parser.add_argument("--top_k", type=int, help="Top-k")
    parser.add_argument("--max_tokens", type=int, default=2048, help="Max tokens")
    parser.add_argument("--presence_penalty", type=float, help="Presence penalty")
    parser.add_argument("--repetition_penalty", type=float, help="Repetition penalty")

    # TACO-specific parameters
    parser.add_argument(
        "--difficulties", default="ALL", help="Comma-separated difficulties or ALL"
    )
    parser.add_argument("--skills", default="ALL", help="Comma-separated skills or ALL")
    parser.add_argument(
        "--n_samples", type=int, default=1, help="Number of samples per problem"
    )
    parser.add_argument(
        "--max_workers", type=int, default=4, help="Max concurrent workers"
    )
    parser.add_argument(
        "--timeout", type=int, default=300, help="Request timeout in seconds"
    )

    return parser.parse_args()
