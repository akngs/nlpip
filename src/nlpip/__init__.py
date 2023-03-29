import hashlib
import json
import os
import re
import sys
from pathlib import Path

import openai

HOME = str(Path.home())
SCRIPT_HOME = os.path.dirname(os.path.realpath(__file__))

def main():
    """Run a prompt"""
    if len(sys.argv) != 2:
        print("Usage: nlpip <prompt_id>", file=sys.stderr)
        sys.exit(1)
    prompt_id = sys.argv[1]

    api_key = os.getenv("OPENAI_API_KEY", None)
    if api_key is None:
        print("Please set OPENAI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)
    openai.api_key = api_key

    try:
        template = _load_template(prompt_id)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    stdin_text = "\n".join(sys.stdin.readlines())
    prompt = _merge_template(template, stdin_text)
    answer = _ask(prompt)
    return re.sub(r"\n\n", "\n", answer)


def _load_template(prompt_id):
    user_path = os.path.join(HOME, ".nlpip", "prompts", f"{prompt_id}.txt")
    if os.path.exists(user_path):
        with open(user_path, encoding="utf-8") as f:
            return f.read()

    builtin_path = os.path.join(SCRIPT_HOME, "prompts", f"{prompt_id}.txt")
    if os.path.exists(builtin_path):
        with open(builtin_path, encoding="utf-8") as f:
            return f.read()

    raise ValueError(f"Prompt '{prompt_id}'` not found")


def _merge_template(template, stdin_text):
    if template.find("{{STDIN}}") != -1:
        merged = template.replace("{{STDIN}}", stdin_text)
    else:
        merged = template + "\n--- START ---\n" + stdin_text + "\n--- END ---\n"

    return merged


def _ask(prompt):
    params = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You should answer in clear, concise way.",
            },
            {
                "role": "system",
                "content": (
                    "Sentences like '--- START ---' and '--- END ---' are just separators "
                    "for you. Never include them in your answer."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }

    cache_key = hashlib.sha256(json.dumps(params).encode("utf-8")).hexdigest()
    cached_answer = _load_cache(cache_key)
    if cached_answer:
        return cached_answer

    res = openai.ChatCompletion.create(**params)
    answer = res["choices"][0]["message"]["content"].strip()
    _save_cache(cache_key, answer)

    return answer


def _load_cache(cache_key):
    cache_dir = os.path.join(HOME, ".nlpip", "caches", cache_key[:2])
    os.makedirs(cache_dir, exist_ok=True)

    cache_path = os.path.join(cache_dir, cache_key[2:])
    if not os.path.exists(cache_path):
        return None

    with open(cache_path, encoding="utf-8") as f:
        return f.read()


def _save_cache(cache_key, answer):
    cache_dir = os.path.join(HOME, ".nlpip", "caches", cache_key[:2])
    os.makedirs(cache_dir, exist_ok=True)

    cache_path = os.path.join(cache_dir, cache_key[2:])
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(answer)


if __name__ == "__main__":
    main()
