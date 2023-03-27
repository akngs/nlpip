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
            prompt = (
                prompt_template + "\n--- START ---\n" + input_text + "\n--- END ---\n"
            )

        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        print(res["choices"][0]["text"].strip())


if __name__ == "__main__":
    fire.Fire(CLI)
