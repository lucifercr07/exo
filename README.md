# exo

Toolings and scripts for statistics and communication for DiceDB.

```
pip install -r requirements.txt
cp .env.sample .env
```

Update the `.env` file with required tokens, secrets, and credentails.

### Create issue on GitHub to support a Redis Command

```
python scripts/create_issue_redis_cmd.py <REDIS_COMMAND_NAME>
```

### Refresh GitHub Pull Requests in DB

```
python refresh_prs.py
```

### Create issue on GitHub for a TCL test error

#### Prerequisites
- [Git](https://git-scm.com/) (for cloning the repository)
- [Go](https://golang.org/doc/install) (for running the server)
- TCL (for running the tests)

#### To install Go and Git:

```bash
# Install Git
sudo apt-get install git

# Install Go
sudo apt install golang-go
```

#### To run the TCL tests in the dice-tests repository and post issues:
1. ```python create_issue_tcl_tests.py -h``` - Help on usage of script
2. ```python create_issue_tcl_tests.py``` - To clone the master repo and generate issues out of tests.
3. ```python create_issue_tcl_tests.py --dice_tests_repo_path /path/to/local-dice-tests-repo``` - To run script on local dice-tests repo and generate issues.
4. ```python create_issue_tcl_tests.py --dry_run``` - For dry run.
5. ```python create_issue_tcl_tests.py --post_issue``` - To post a GitHub issue for a specific TCL error.

## Lint

```
make lint
```

