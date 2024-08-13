import os
import sys

import mdformat
from openai import OpenAI

if os.environ.get("OPENAI_API_KEY") is None:
    print("Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)

client = OpenAI()


def generate_doc(command: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are a software engineer who knows how to write great documentation.
                    
                    Write an extremely detailed and elaborated documentation for the following
                    Redis command. Make sure you have a section for parameters, one section
                    for return value, and one section for example usage of command. Also add sections
                    such as Behaviour covering what would happen when this command is fired,
                    and Error Handling covering the cases in which error will be raised.
                    Also specify what error will be raised.""",
            },
            {
                "role": "user",
                "content": f"Write documentation for the Redis command: {command}",
            },
        ],
    )

    return completion.choices[0].message.content


def main():
    out_dirpath = sys.argv[1]
    command = sys.argv[2]
    command = command.upper()

    doc = generate_doc(command)
    doc = doc.replace("**", "`")
    doc = doc.replace("Redis", "DiceDB")
    doc = doc.replace("redis", "DiceDB")
    doc = mdformat.text(doc)

    filepath = os.path.join(out_dirpath, f"{command}.md")
    with open(filepath, "w") as f:
        f.write(
            f"""---
title: "{command}"
description: "Documentation for the Redis command {command}"
---

{doc}
"""
        )


if __name__ == "__main__":
    main()
