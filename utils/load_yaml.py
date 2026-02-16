from pathlib import Path

import yaml


def load_question_agent_prompts():
    prompts_path = Path(__file__).parent / "prompts" / "question_agent.yaml"
    with open(prompts_path, encoding='utf-8') as f:
        return yaml.safe_load(f)
