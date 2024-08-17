# pylint: disable=line-too-long
import mdformat
import requests

from config import GITHUB_TOKEN

def create_github_issue(cmd: str,):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    description = f"""
This issue is all about ensuring we are as close to Redis as possible. The command in focus for this issue is `{cmd}`.

Go through the [official documentation](https://redis.io/docs/latest/commands) of the command `{cmd}` on Redis and identify the inconsistencies. The inconsistencies could be in

1. unhandled edge case
2. unexpected behavior
3. unsupported option

Because we are trying to be compatible with Redis v7.2.5, I would recommend you try out different variants of the command with different inputs on that specific version. The instructions on running Redis v7.2.5 locally

- [from source code](https://gist.github.com/arpitbbhayani/94aedf279349303ed7394197976b6843)
- [use Docker](https://hub.docker.com/_/redis)

Once you find the discrepancy, you can either

1. raise an issue on [Dice repository](https://github.com/dicedb/dice) with details, or
2. try to fix it yourself and raise a PR

If you are [raising the issue](https://github.com/DiceDB/dice/issues/new?assignees=&labels=&projects=&template=inconsistent_dicedb_vs_redis.md&title=Inconsistent+%60%7BCMD%7D%60%3A+%3CDescribe+the+error+in+one+concise+line%3E), make sure you provide the details such as

0. [use the template](https://github.com/DiceDB/dice/issues/new?assignees=&labels=&projects=&template=inconsistent_dicedb_vs_redis.md&title=Inconsistent+%60%7BCMD%7D%60%3A+%3CDescribe+the+error+in+one+concise+line%3E) and provide the following details
1. steps to reproduce (series of commands)
2. observed output on DiceDB
3. observed output on Redis v7.2.5

Also, feel free to update the documentation and raise the PR in the [docs repository](https://github.com/dicedb/docs).

> You will need to go deeper into the command make sure you are covering all cases and reporting the inconsistencies or fixing them. The deeper the work, the better our stability will be. Also, it is possible that we do not find any discrepancies, so please mention the same in the comment on this issue. Mention the PR or issue links that you create under this issue.
"""
    description = mdformat.text(description)
    title = f"Report inconsistency in the command `{cmd}`"

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
    create_github_issue(command)
