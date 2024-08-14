# pylint: disable=line-too-long
import os
import sys

import mdformat
import requests
from openai import OpenAI

from config import GITHUB_TOKEN

if os.environ.get("OPENAI_API_KEY") is None:
    print("Please set the OPENAI_API_KEY environment variable.")
    sys.exit(1)


client = OpenAI()


def generate_title(description: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.0,
        messages=[
            {
                "role": "user",
                "content": f"""Extract the core error or inconsistency and explain it in less than 80 characters without using the words DiceDB or Redis.
                
                {description}""",
            },
        ],
    )

    return completion.choices[0].message.content


def create_github_issue(
    cmd: str, steps_to_reproduce: str, redis_output: str, dicedb_output: str
):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    description = f"""
The command `{cmd}` is not consistent with Redis implementation. Here are the steps to reproduce the issue

```
{steps_to_reproduce}
```

Here's the output I observed in Redis v7.2.5

```
{redis_output}
```

and here's the output I observed in DiceDB's latest commit of the `master` branch

```
{dicedb_output}
```

Make the implementation consistent with the Redis implementation.
Make sure you are using Redis version 7.2.5 as a reference for the
command implementation and to setup Redis from source,
you can follow [these instructions](https://gist.github.com/arpitbbhayani/94aedf279349303ed7394197976b6843).
"""
    description = mdformat.text(description)
    title = generate_title(description)

    data = {"title": title, "body": description}

    response = requests.post(
        "https://api.github.com/repos/DiceDB/dice/issues",
        json=data,
        headers=headers,
        timeout=10,
    )
    if response.status_code == 201:
        print(f"Successfully created issue: {title}")
    else:
        print(f"Failed to create issue: {title}")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")


def multiline_input() -> str:
    print("press Enter twice to complete your input")
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return "\n".join(lines)


if __name__ == "__main__":
    command = input("Enter the command that is inconsistent:")

    print("Enter the commands in order to reproduce the issue:")
    steps_to_reproduce = multiline_input()

    print("Enter the output you observe in Redis:")
    redis_output = multiline_input()

    print("Enter the output you observe in DiceDB:")
    dicedb_output = multiline_input()

    create_github_issue(command, steps_to_reproduce, redis_output, dicedb_output)
