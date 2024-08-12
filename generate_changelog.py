from dao.pull_requests import get_pull_requests

all_prs = get_pull_requests("DiceDB", "dice")
print("Total PRs", len(all_prs))
print("Contributors", len(set([pr.contributor.id for pr in all_prs])))

for index, pr in enumerate(all_prs):
    print(pr.title)
    print(pr.contributor.name, f"@{pr.contributor.twitter_username}")
    print(f"If you are interested to peek into the change, here's the PR {pr.url}")
    print("\n--------\n")
