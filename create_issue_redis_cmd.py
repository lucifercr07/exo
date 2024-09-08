# pylint: disable=line-too-long
import sys

import requests

from config import GITHUB_TOKEN

def get_title_body(cmd):
    title = f"Add support for command `{cmd}`"
    body = f"""Add support for the `{cmd}` command in DiceDB similar to the [`{cmd}` command in Redis](https://redis.io/docs/latest/commands/command-list/). Please refer to the following commit in Redis to understand the implementation specifics - [source](https://github.com/redis/redis/tree/f60370ce28b946c1146dcea77c9c399d39601aaa).

    Write unit and integration tests for the command referring to the tests written in the [Redis codebase 7.2.5](https://github.com/redis/redis/tree/f60370ce28b946c1146dcea77c9c399d39601aaa). For integration tests, you can refer to the `tests` folder. Note: they have used `TCL` for the test suite, and we need to port that to our way of writing integration tests using the relevant helper methods. Please refer to our [tests directory](https://github.com/DiceDB/dice/tree/master/tests).

    For the command, benchmark the code and measure the time taken and memory allocs using [`benchmem`](https://blog.logrocket.com/benchmarking-golang-improve-function-performance/) and try to keep them to the bare minimum.
    """
    return title, body


def create_github_issue(cmd):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    title, body = get_title_body(cmd)
    data = {"title": title, "body": body}

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


if __name__ == "__main__":
    cmd = sys.argv[1]

#     cmds = """
# JSON.ARRAPPEND
# JSON.ARRINDEX
# JSON.ARRINSERT
# JSON.ARRLEN
# JSON.ARRPOP
# JSON.ARRTRIM
# JSON.DEBUG
# JSON.DEBUG HELP
# JSON.DEBUG MEMORY
# JSON.FORGET
# JSON.MGET
# JSON.NUMINCRBY
# JSON.NUMMULTBY
# JSON.OBJKEYS
# JSON.OBJLEN
# JSON.RESP
# JSON.STRAPPEND
# JSON.STRLEN
# JSON.TOGGLE
# """.split("\n")

    # for cmd in cmds:
    #     cmd = cmd.strip()
    #     if not cmd:
    #         continue
    create_github_issue(cmd)
