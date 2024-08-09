import os

from dao.contributors import create_contributor, get_contributor
from dao.pull_requests import create_pull_request
from svc.github import get_contributor_github, get_merged_pull_requests_github

token = os.environ.get("GITHUB_TOKEN")


def main():
    page = 1
    while True:
        merged_prs = get_merged_pull_requests_github("DiceDB", "dice", page=page)
        if not merged_prs:
            break
        for pr in merged_prs:
            if get_contributor(pr.contributor_id) is None:
                contributor = get_contributor_github(pr.contributor_username)
                create_contributor(contributor)
            create_pull_request(pr)
        if input("should I continue? (y/n): ") == "n":
            break
        page += 1


if __name__ == "__main__":
    main()
