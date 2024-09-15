# Giving Report Data Cleaners for CCB

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

2. Drop your giving csv into this directory and rename the `input_file` variable in your python script

   ```python
   input_file = "<your csv>.csv"
   ```

- Alternatively, you can rename your file to the `input_file` variable default value `"pledge_and_giving_detail.csv"`

- NOTE: do not check in sensitive file names

## Run Formatter

```bash
# Format the provided data into two CSVs: one for members who have pledged and one for members who have not pledged but have given.
python3 giving-breakdown.py
```
