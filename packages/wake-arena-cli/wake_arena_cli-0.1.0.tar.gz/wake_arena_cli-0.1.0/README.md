# Wake Arena CLI
Wake Arena command line interface to operate projects and vulnerability checks.

## Setup
1. Activate the venv
```shell
poetry shell
```
2. Install dependencies
```shell
poetry install
```
3. Run the cli module
```shell
python -m cli
```

## Env parameters
| Env                   | Description                                                      |
|-----------------------|------------------------------------------------------------------|
| `WAKE_ARENA_API_KEY`  | Uses api key instead of configured authentication                |
| `WAKE_ARENA_PROJECT`  | Project id. CLI will use this project instead of configured one  |
| `WAKE_ARENA_API_URL`  | Development only, replaces Wake Arena API endpoint for cli       |
| `WAKE_ARENA_WEB_URL`  | Development only, replaces Wake Arena WEB url for cli            |