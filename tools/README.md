# Tools

- `environments.py` updates `static/data/environments.json`.
- `examples.py` updates `static/data/examples.json`.
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

## Examples

The examples catalog rendered at `/examples` is built from the per-language
`examples.json` files in the [fission/examples](https://github.com/fission/examples)
repository (one next to each language's samples, plus the ones under
`miscellaneous/`). `examples.py` reads those files, groups them by language, adds
the catalog logos and group tags, and writes `static/data/examples.json`.

Clone `fission/examples` and regenerate (run from this `tools/` directory):
```
python3 examples.py /path/to/fission-examples
```
The path argument defaults to a sibling checkout at `../../examples`. Commit the
updated `static/data/examples.json`.

To add a new example, add an entry to the relevant `examples.json` in the
`fission/examples` repo, then rerun the script. New languages or logos are
configured in the `GROUPS` list in `examples.py`.

## ChangeLog
Copy the changelog section from draft release to a file `notes.txt`.
Run `notes.py` on it.
```
python3 notes.py
```
