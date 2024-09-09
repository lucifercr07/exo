# pylint: disable=line-too-long
import sys

import requests

from config import GITHUB_TOKEN
import datetime

def get_current_timestamp():
    current_timestamp = datetime.datetime.now().isoformat()
    return current_timestamp


def store_since(since):
    with open('./state/comments_on_inactive_issues_since.txt', 'w') as file:
        file.write(since)


def load_since():
    with open('./state/comments_on_inactive_issues_since.txt', 'r') as file:
        return file.read()


since = load_since()

def get_issues():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    issues = []
    page = 1
    per_page = 3

    while True:
        response = requests.get(
            f"https://api.github.com/repos/DiceDB/dice/issues?sort=updated&direction=asc&per_page={per_page}&page={page}&since={since}",
            headers=headers,
            timeout=10,
        )
        if response.status_code != 200:
            print("Failed to fetch issues", response.status_code)
            print(response.text)
            return

        page_issues = response.json()
        print([issue["number"] for issue in page_issues])
        # issues.extend(page_issues)
        if len(page_issues) < per_page:
            break
        page += 1

    return issues

# def post_update_comment(issue_number, assignee):
#     headers = {
#         "Authorization": f"token {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json",
#     }

#     comment = f"Hey @{assignee}, just wanted to provide an update on this issue."
#     data = {"body": comment}

#     response = requests.post(
#         f"https://api.github.com/repos/DiceDB/dice/issues/{issue_number}/comments",
#         json=data,
#         headers=headers,
#         timeout=10,
#     )
#     if response.status_code == 201:
#         print("Successfully posted update comment")
#     else:
#         print("Failed to post update comment")
#         print(f"Status code: {response.status_code}")
#         print(f"Response: {response.text}")

for issue in get_issues():
    issue_number = issue["number"]
    assignee = issue["assignee"]["login"] if issue["assignee"] else ""
    print(issue_number, assignee)
    # post_update_comment(issue_number, assignee)

store_since(get_current_timestamp())
