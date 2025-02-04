# Data Cleaners for CCB

## Requirements:

- Python3
- pip3

- To install these dependencies

  ```bash
  brew install python3
  ```

## Init Environment:

1. Create a virtual environment for pandas

   ```bash
   python3 -m venv deps
   source deps/bin/activate
   python3 -m pip install pandas
   ```

   - If "deps/" exists in your environment, only activate the venv

     ```bash
     source deps/bin/activate
     ```

2. Drop your giving csv into this directory and rename the `families_file` and `givings_file` variables in your python script

   ```python
   families_file = "<your csv>.csv"
   givings_file = "<your csv>.csv"
   ```

- NOTE: do not check in sensitive file names

## Run Formatter

```bash
python3 split.py
```
