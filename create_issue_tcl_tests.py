import argparse
import os
import re
import shutil
import subprocess

import mdformat
import requests

from config import GITHUB_TOKEN

DICE_CMDS = ['PING', 'AUTH', 'SET', 'GET', 'MSET', 'JSON.SET', 'JSON.GET', 'JSON.TYPE', 'JSON.CLEAR', 'JSON.DEL',
             'JSON.FORGET', 'JSON.ARRLEN', 'TTL', 'DEL', 'EXPIRE', 'EXPIRETIME', 'EXPIREAT', 'HELLO', 'BGREWRITEAOF',
             'INCR', 'INFO', 'CLIENT', 'LATENCY', 'LRU', 'SLEEP', 'BFINIT', 'BFADD', 'BFEXISTS', 'BFINFO', 'SUBSCRIBE',
             'QWATCH', 'QUNWATCH', 'MULTI', 'EXEC', 'DISCARD', 'ABORT', 'COMMAND', 'SETBIT', 'GETBIT', 'BITCOUNT',
             'BITOP', 'KEYS', 'MGET', 'PERSIST', 'COPY', 'DECR', 'EXISTS', 'GETDEL', 'DECRBY', 'RENAME', 'GETEX',
             'PTTL', 'HSET', 'OBJECT', 'TOUCH', 'LPUSH', 'RPOP', 'RPUSH', 'LPOP', 'DBSIZE', 'GETSET', 'FLUSHDB',
             'BITPOS', 'SADD', 'SMEMBERS', 'SREM', 'SCARD', 'SDIFF', 'SINTER', 'HGETALL', 'PFADD', 'PFCOUNT', 'HGET',
             'PFMERGE']
DICE_TESTS_REPO_LINK = "https://github.com/AshwinKul28/dice-tests/tree/main"
DICE_TESTS_REPO_URL = "git@github.com:AshwinKul28/dice-tests.git"
DICE_REPO_URL = "https://api.github.com/repos/DiceDB/dice/issues"
TCL_TEST_OUTPUT_FILE_NAME = "tcl_test_run_output.txt"
ERR_PREFIX = '[err]'
OK_PREFIX = '[ok]'
IGNORE_PREFIX = '[ignore]'
STEPS_TO_REPRODUCE_SENTENCE = ("Run the commands mentioned in the test on Line {line_number} in the file {"
                               "repo_link}#L{line_number}.")


def validate_no_empty_vars(*args):
    for arg in args:
        if arg is None or arg == '':
            return False
    return True


def find_line_number(file_path, search_string):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines, start=1):
        if 'BITCOUNT against test vector #' in line:
            search_string = 'BITCOUNT against test vector #'

        if search_string in line:
            return i
    return None


def extract_tcl_file_name_and_description(error_message):
    # Find the last occurrence of "in" and extract the TCL file name after it
    match = re.search(r'(.*)\s+in\s+([^\s]+\.tcl)', error_message)
    if match:
        prefix = match.group(1).strip()
        file_name = match.group(2).strip()
        return prefix, file_name
    return None, None


def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1b\[([0-9;]*m)')
    return ansi_escape.sub('', text)


def parse_errors_from_file(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    lines = [strip_ansi_codes(line) for line in lines]
    tcl_test_errors = []
    current_error = []
    in_error_block = False

    # Iterate through each line
    for line in lines:
        if line.startswith(ERR_PREFIX):
            if in_error_block:
                tcl_test_errors.append(''.join(current_error))
                current_error = []
            in_error_block = True
            line = line.replace('[err]: ', '').strip()
        elif (line.startswith(OK_PREFIX) or line.startswith(IGNORE_PREFIX)) and in_error_block:
            tcl_test_errors.append(''.join(current_error))
            current_error = []
            in_error_block = False

        if in_error_block:
            current_error.append(line + '\n')

    if current_error:
        tcl_test_errors.append(''.join(current_error))

    return tcl_test_errors


def create_issue_title_and_description(cmd, title_cmd_description, steps_to_reproduce, expected_output,
                                       observed_output):
    if not validate_no_empty_vars(cmd, title_cmd_description, steps_to_reproduce,
                                  expected_output,
                                  observed_output):
        print("FAILED to generate/post issue for error, value empty or None")
        return

    if cmd in DICE_CMDS:
        issue_title = f"""Inconsistent `{cmd}`: {title_cmd_description}"""
    else:
        issue_title = f"""{title_cmd_description}"""

    description = f"""
## Steps to reproduce

{steps_to_reproduce}

## Expected output

The expected output when the above set of commands when run on Redis

```
{expected_output}
```

## Observed output

The observed output when the above set of commands when run on DiceDB

```
{observed_output}
```

The steps to run the test cases are mentioned in the README of the [dice-tests repository](https://github.com/AshwinKul28/dice-tests).


## Expectations for resolution

This issue will be considered resolved when the following things are done:

1. Changes in the [`dice`](https://github.com/dicedb/dice) repository code to meet the expected behavior.
2. Successful run of the tcl test behavior.

You can find the tests under the `tests` directory of the [`dice`](https://github.com/dicedb/dice) repository and the steps to run are in the [README file](https://github.com/dicedb/dice). Refer to the following links to set up DiceDB and Redis 7.2.5 locally

- [Setup DiceDB locally](https://github.com/dicedb/dice)
- [Setup Redis 7.2.5 locally](https://gist.github.com/arpitbbhayani/94aedf279349303ed7394197976b6843)
- [Setup DiceDB CLI](https://github.com/dicedb/dice)
"""
    description = mdformat.text(description)

    return issue_title, description


def create_issues(tcl_tests_errors, dice_tests_path):
    issue_templates = []

    for error in tcl_tests_errors:
        error_with_description = error.split('\n')[0]
        error_details = error.split('\n')[1]
        cmd = error_with_description.split(' ')[0]
        issue_description, tcl_file_name = extract_tcl_file_name_and_description(error_with_description)
        line_number = find_line_number(dice_tests_path + '/' + tcl_file_name, issue_description)
        steps_to_reproduce = STEPS_TO_REPRODUCE_SENTENCE.format(line_number=line_number, repo_link=DICE_TESTS_REPO_LINK)
        if "to equal or match" in error_details:
            expected_output = error_details.replace('Expected ', '').split(' to equal or match ')[0]
            observed_output = error_details.split(' to equal or match ')[1]
        elif "==" in error_details:
            expected_output = error_details.split(' == ')[0]
            observed_output = error_details.split(' == ')[1]
        else:
            expected_output = error_details
            observed_output = error_details

        if not validate_no_empty_vars(cmd, issue_description, steps_to_reproduce,
                                      expected_output,
                                      observed_output):
            print("FAILED to generate/post issue for error ", error)
            continue

        issue_title, issue_description = create_issue_title_and_description(cmd, issue_description, steps_to_reproduce,
                                                                            expected_output,
                                                                            observed_output)
        issue_templates.append([issue_title, issue_description])

    return issue_templates


def clone_or_replace_repo(repo_url, clone_path):
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)
        print(f"Removed existing directory at {clone_path}")

    try:
        subprocess.run(["git", "clone", repo_url, clone_path], check=True)
        print(f"Cloned repository to {clone_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")
        exit(1)


def run_tcl_tests_and_check_output(dice_tests_repo_path):
    # Change the current working directory to the dice-tests path
    os.chdir(dice_tests_repo_path)
    # If some old test output file exists remove it
    output_file_path = os.path.join(dice_tests_repo_path, TCL_TEST_OUTPUT_FILE_NAME)
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    # Execute tcl test suite
    try:
        subprocess.run(["./tcltest > tcl_test_run_output.txt"], shell=True, check=True)
        print("Executed ./tcltest command.")
    except subprocess.CalledProcessError as e:
        if not os.path.exists(output_file_path):
            print(f"Failed to execute ./tcltest command: {e}")
            exit(1)

    print(f"The file 'tcl_test_run_output.txt' was created successfully at {output_file_path}.")

    return output_file_path


def create_github_issue(title, description):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"title": title, "body": description}
    response = requests.post(
        DICE_REPO_URL,
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


def setup(dice_tests_repo_path):
    if os.path.exists(args.dice_tests_repo_path):
        dice_tests_repo_path = args.dice_tests_repo_path
        if not os.path.exists(dice_tests_repo_path):
            print("Dice tests repo path not found at: " + dice_tests_repo_path)
            exit(1)
    else:
        # Clone the repository of dice_tests
        current_dir = os.getcwd()
        dice_tests_repo_path = os.path.join(current_dir, "dice-tests")
        clone_or_replace_repo(DICE_TESTS_REPO_URL, dice_tests_repo_path)

    file_path = run_tcl_tests_and_check_output(dice_tests_repo_path)

    return file_path, dice_tests_repo_path, bool(args.dry_run)


def setup_post_issue():
    return bool(args.post_issue)


if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("GitHub token not found, please set the GITHUB_TOKEN environment variable.")
        exit(1)

    parser = argparse.ArgumentParser(description="Process dice TCL issues.")
    parser.add_argument('--dice_tests_repo_path', help='Path to the dice tests local directory')
    parser.add_argument('--dry_run', action='store_true', help='Enable for dry run')
    parser.add_argument('--post_issue', action='store_true', help='Given TCL error message and expected output, posts '
                        'issue to dice repo')
    args = parser.parse_args()
    post_issues_only = bool(args.post_issue)
    if post_issues_only:
        tcl_error_statement = input("Enter TCL error statement from output file. e.g: [err]: SET with EX with big "
                                    "integer should report an error in tcltests/unit/expire.tcl")
        if not tcl_error_statement.startswith("[err]: "):
            print("Invalid TCL error statement. Should start with '[err]'")
            exit(1)

        tcl_error_statement = tcl_error_statement.replace("[err]: ", '')
        tcl_expected_output = input("Enter expected output. e.g: ERR invalid expire time in 'set' command")
        tcl_observed_output = input("Enter observed output. e.g: OK")
        tcl_dice_tests_repo_path = input("Enter dice-tests repo absolute path. e.g: OK")
        issue_description, tcl_file_name = extract_tcl_file_name_and_description(tcl_error_statement)
        cmd = tcl_error_statement.split(' ')[0]
        line_number = find_line_number(tcl_dice_tests_repo_path + '/' + tcl_file_name, issue_description)
        steps_to_reproduce = STEPS_TO_REPRODUCE_SENTENCE.format(line_number=line_number, repo_link=DICE_TESTS_REPO_LINK)
        issue_title, issue_description = create_issue_title_and_description(cmd, issue_description, steps_to_reproduce,
                                                                            tcl_expected_output, tcl_observed_output)
        print(issue_title)
        print(issue_description)
        print('-----------------------')
        confirm = input("Want to post above issue to dice repo? (y/n)")
        if confirm == 'y':
            create_github_issue(issue_title, issue_description)
        exit(0)
    elif args.dice_tests_repo_path:
        tcl_test_run_output_file_path, dice_tests_path, dry_run = setup()
        tcl_tests_errors = parse_errors_from_file(tcl_test_run_output_file_path)
        all_issues = create_issues(tcl_tests_errors, dice_tests_path)
        print("Total issues found: ", len(all_issues))
        if len(all_issues) == 0:
            print("No issues found!!! Happy life!!!! :)")
            exit(0)

        for title, description in all_issues:
            print(title)
            print(description)
            print('-----------------------')
            if not dry_run:
                confirm = input("Want to post above issue to dice repo? (y/n)")
                if confirm == 'y':
                    create_github_issue(title, description)
            else:
                print("Dry run enabled, skipping GitHub issue creation.")
    else:
        parser.print_help()
