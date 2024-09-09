# pylint: disable=line-too-long
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

def foo():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    issues = []
    page = 1
    per_page = 30

    while True:
        response = requests.get(
            f"https://api.github.com/repos/DiceDB/dice/issues?sort=updated&direction=asc&per_page={per_page}&page={page}",
            headers=headers,
            timeout=10,
        )
        if response.status_code != 200:
            print("Failed to fetch issues", response.status_code)
            print(response.text)
            return

        issues = response.json()
        for issue in issues:
            if (datetime.datetime.now() - datetime.datetime.strptime(issue["updated_at"], "%Y-%m-%dT%H:%M:%SZ")).days < 5:
                return
            if not issue["assignee"]:
                continue
            print(issue["number"], issue["assignee"]["login"], issue["html_url"], issue["title"])
            post_update_comment(issue["number"], issue["assignee"]["login"])
        page += 1

def post_update_comment(issue_number, assignee):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    comment = f"""Hello @{assignee},

There has been no activity on this issue for the past 5 days.
It would be awesome if you keep posting updates to this issue so that we know you are actively working on it.

We are really eager to close this issue at the earliest, hence if we continue to see the inactivity, we will have to reassign the issue to someone else. We are doing this to ensure that the project maintains its momentum and others are not blocked on this work.

Just drop a comment with the current status of the work or share any issues you are facing. We can always chip in to help you out.

Thanks again.
"""
    data = {"body": comment}

    response = requests.post(
        f"https://api.github.com/repos/DiceDB/dice/issues/{issue_number}/comments",
        json=data,
        headers=headers,
        timeout=10,
    )
    if response.status_code != 201:
        print("Failed to post update comment")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == '__main__':
    foo()
