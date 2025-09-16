"""
TACO Evaluator - Core evaluation logic using OpenAi-compatible API with vLLM
"""

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

import httpx
from openai import OpenAI

# EOF strings for truncation (from original TACO)
EOF_STRINGS = ["\nQUESTION", "\n---", "\nANSWER", "<|endoftext|>"]


def truncate_after_eof_strings(text: str) -> str:
    """Truncate generated text at EOF markers"""
    pattern = "|".join(re.escape(s) for s in EOF_STRINGS)
    match = re.search(pattern, text)

    if match:
        return text[: match.start()]
    else:
        return text


class TACOEvaluator:
    def __init__(
        self,
        base_url: str,
        model_name: str,
        api_key: str,
        temperature: float = None,
        top_p: float = None,
        top_k: int = None,
        max_completion_tokens: int = 2048,
        presence_penalty: float = None,
        repetition_penalty: float = None,
        # we add a 5 minute timeout by default
        timeout: int = 300,
    ):
        """
        Initialize TACO evaluator with OpenAI client following EvalHub patterns

        Args:
            base_url: vLLM API endpoint (e.g., http://host:port/v1)
            model_name: Model name to use
            api_key: API key
            temperature: (optional)
            top_p: Top-p (optional)
            top_k: Top-k (optional)
            max_completion_tokens: (optional)
            presence_penalty:  (optional)
            repetition_penalty: Repetition penalty (optional)
            timeout: Request timeout in seconds
        """
        self.model_name = model_name
        self.timeout = timeout

        # Initialize OpenAI client with custom base_url (EvalHub pattern)
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            http_client=httpx.Client(verify=True, timeout=timeout),
        )

        # Build generation parameters following LCB parameter mapping pattern
        self.generation_params = {
            "model": model_name,
            "max_completion_tokens": max_completion_tokens,
            "stream": False,
        }

        # Add optional parameters if provided
        if temperature is not None:
            self.generation_params["temperature"] = temperature
        if top_p is not None:
            self.generation_params["top_p"] = top_p
        if presence_penalty is not None:
            self.generation_params["presence_penalty"] = presence_penalty

        # vLLM-specific parameters go in extra_body (following LCB pattern)
        extra_body = {}
        if top_k is not None:
            extra_body["top_k"] = top_k
        if repetition_penalty is not None:
            extra_body["repetition_penalty"] = repetition_penalty

        if extra_body:
            self.generation_params["extra_body"] = extra_body

    def generate_single(self, prompt: str, seed: int = None) -> str:
        """Generate a single response for the given prompt with optional seed"""
        try:
            # Add seed to generation params if provided (for reproducibility)
            generation_params = self.generation_params.copy()
            if seed is not None:
                if "extra_body" not in generation_params:
                    generation_params["extra_body"] = {}
                generation_params["extra_body"]["seed"] = seed

            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}], **generation_params
            )

            generated_text = response.choices[0].message.content
            return truncate_after_eof_strings(generated_text)

        except Exception as e:
            print(f"Error generating response: {e}")
            return ""

    def generate_batch(self, prompt: str, n_samples: int, max_workers: int = 4) -> List[str]:
        """Generate multiple samples for a prompt using parallel workers with seeds"""
        if n_samples == 1:
            return [self.generate_single(prompt, seed=0)]

        # Use ThreadPoolExecutor for parallel generation (following EvalHub pattern)
        generations = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks with different seeds for reproducibility (like original TACO)
            futures = [
                executor.submit(self.generate_single, prompt, seed=i) for i in range(n_samples)
            ]

            # Collect results as they complete
            for future in as_completed(futures):
                try:
                    result = future.result()
                    generations.append(result)
                except Exception as e:
                    print(f"Error in batch generation: {e}")
                    generations.append("")

        return generations
