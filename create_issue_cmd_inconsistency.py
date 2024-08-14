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
                "role": "system",
                "content": """I want you to act as a title generator for GitHub issue based on description.
                    
                    I will provide you with the description of the issue in the markdown format,
                    and you will generate one concise and relevant title ensuring that the meaning is maintained.
                    The title should be short and to the point, and should not exceed 100 characters
                """,
            },
            {
                "role": "user",
                "content": f"Here's the description of the issue:\n\n{description}",
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
I found that the command `{cmd}` is not consistent with Redis implementation and
it behaves differently in DiceDB as compared to Redis. Here are the steps to reproduce the command

```
{steps_to_reproduce}
```

Here's the output I observe in Redis v7.2.5

```
{redis_output}
```

and here's the output I observe in DiceDB latest version of `master` branch

```
{dicedb_output}
```

We need to look into the issue and fix the command and make it consistent with the Redis implementation.
Make sure you are using Redis version 7.2.5 as a reference for the command implementation.
To setup Redis v7.2.5 from source, you can run the following commands in your Ubuntu/Mac/WSL environment

```sh
git clone https://github.com/redis/redis/
cd redis
git checkout 7.2.5
make
cd src
./redis-server
```

Once you have the Redis server running, you can test the command using the steps mentioned above and compare the output with DiceDB.
To setup DiceDB locally please follow the steps mentioned under [Setting up DiceDB from source for development and contributions](https://github.com/DiceDB/dice/blob/master/README.md#setting-up-dicedb-from-source-for-development-and-contributions) section of README.md file of the repository.
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
