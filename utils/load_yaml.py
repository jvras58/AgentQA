from pathlib import Path

import yaml


def load_prompts_from_yaml(filename: str):
    prompts_path = Path(__file__).parent / "prompts" / filename
    with open(prompts_path, encoding='utf-8') as f:
        return yaml.safe_load(f)
