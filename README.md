# exo

Toolings and scripts for statistics and communication for DiceDB.

```
pip install -r requirements.txt
cp .env.sample .env
```

Update the `.env` file with required tokens, secrets, and credentails.

### Create issue on GitHUb to support a Redis Command

```
python scripts/create_issue_redis_cmd.py <REDIS_COMMAND_NAME>
```

### Refresh GitHub Pull Requests in DB

```
python refresh_prs.py
```

## Lint

```
make lint
```
