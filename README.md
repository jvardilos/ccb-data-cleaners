# Giving Report Data Cleaners for CCB

## Requirements:

- Python3
- pip3

- install these dependencies

```bash
brew install python3
```

## Init Environment:

```bash
python3 -m venv deps
source deps/bin/activate
python3 -m pip install pandas
```

- When running again, only activate the venv

```bash
source deps/bin/activate
```

## Run Formatter

```bash
# format the giving data into only the essential columns for emailing users
python3 giving-breakdown.py
```
