import hashlib
import json
import os
import sys
from pathlib import Path

import fire
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class CLI:
    """Natural Language Pipe"""

    def run(self, prompt_id):
        """Run a prompt"""
        template = self._load_template(prompt_id)
        stdin_text = "\n".join(sys.stdin.readlines())
        prompt = self._merge_template(template, stdin_text)
        answer = self._ask(prompt)
        print(answer)

    def _load_template(self, prompt_id):
        user_path = os.path.join(
            str(Path.home()), ".nlpipe", "prompts", f"{prompt_id}.txt"
        )
        if os.path.exists(user_path):
            with open(user_path, encoding="utf-8") as f:
                return f.read()

        builtin_path = os.path.join("prompts", f"{prompt_id}.txt")
        if os.path.exists(builtin_path):
            with open(builtin_path, encoding="utf-8") as f:
                return f.read()

        raise ValueError(f"Prompt {prompt_id} not found")

    def _merge_template(self, template, stdin_text):
        if template.find("{{STDIN}}") != -1:
            merged = template.replace("{{STDIN}}", stdin_text)
        else:
            merged = template + "\n--- START ---\n" + stdin_text + "\n--- END ---\n"

        return merged

    def _ask(self, prompt):
        params = {
            "model": "text-davinci-003",
            "prompt": prompt,
            "temperature": 0,
            "max_tokens": 3000,
            "top_p": 1.0,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.0,
        }

        cache_key = hashlib.sha256(json.dumps(params).encode("utf-8")).hexdigest()
        cached_answer = self._load_cache(cache_key)
        if cached_answer:
            return cached_answer

        res = openai.Completion.create(**params)
        answer = res["choices"][0]["text"].strip()
        self._save_cache(cache_key, answer)

        return answer

    def _load_cache(self, cache_key):
        cache_dir = os.path.join(".cache", cache_key[:2])
        os.makedirs(cache_dir, exist_ok=True)

        cache_path = os.path.join(cache_dir, cache_key[:2])
        if not os.path.exists(cache_path):
            return None

        with open(cache_path, encoding="utf-8") as f:
            return f.read()

    def _save_cache(self, cache_key, answer):
        cache_dir = os.path.join(".cache", cache_key[:2])
        os.makedirs(cache_dir, exist_ok=True)

        cache_path = os.path.join(cache_dir, cache_key[:2])
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(answer)


if __name__ == "__main__":
    fire.Fire(CLI)
