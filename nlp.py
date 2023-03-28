import hashlib
import json
import os
import sys

import fire
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class CLI:
    """Natural Language Pipe"""

    def run(self, prompt):
        """Run a prompt"""
        with open(os.path.join("prompts", f"{prompt}.txt"), encoding="utf-8") as f:
            prompt_template = f.read()
            input_text = "\n".join(sys.stdin.readlines())
            prompt = self._merge_command(prompt_template, input_text)

        answer = self._ask(prompt)
        print(answer)

    def _merge_command(self, template, input_text):
        prompt = template + "\n--- START ---\n" + input_text + "\n--- END ---\n"
        return prompt

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
