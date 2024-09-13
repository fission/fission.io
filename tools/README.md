# Tools

- `environments.py` updates `static/data/environments.json`.
- `notes.py` generates content for changelog section in release notes.

## Environments
### Updating the existing environments
Copy [environments.json](https://github.com/fission/environments/blob/master/environments.json) from [environments](https://github.com/fission/environments/tree/master) repository to `tools/` directory.

Update the `static/data/environments.json` by running the command:
```
python3 environments.py
```

### Adding a new environment
Add static data for new environment to `static/data/environments.json`:
Ex: For FastAPI environment
```
    {
        "name": "Python (FastAPI)",
        "logo": "/images/lang-logo/python-logo.svg",
        "repo": "https://github.com/fission/environments/tree/master/python-fastapi",
        "images": []
    },
```

Add a key-value pair for new environment to `environments.py` `env_dict` dictionary.
Where key is the name of new environment in [environments.json](https://github.com/fission/environments/blob/master/environments.json) and
value is the name for new environment in `static/data/environments.json`.
```
    Python FastAPI Environment: Python (FastAPI)
```

Now, run the script.
```
python3 environments.py
```

## ChangeLog
Copy the changelog section from draft release to a file `notes.txt`.
Run `notes.py` on it.
```
python3 notes.py
```
