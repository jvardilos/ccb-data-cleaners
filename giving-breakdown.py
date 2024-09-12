import pandas as pd
from enum import Enum

input_file = "sample.csv"


class Column(Enum):
    NAME = "Name"
    SPOUSE = "Spouse"
    AND_SPOUSE = "Spouse2"
    PLEDGED = "Pledged"
    GIVEN = "Given"
    EMAIL = "Email"


def format_couples(df):
    df[[Column.NAME.value, Column.SPOUSE.value]] = df[Column.NAME.value].str.extract(
        r"(\w+)(?:\s*&\s*(\w+))?", expand=True
    )
    df[Column.AND_SPOUSE.value] = df[Column.SPOUSE.value].apply(
        lambda x: f"and {x}" if pd.notna(x) else ""
    )

    return df


def filter_pledgers_and_givers(df):
    pledged_givers = df[df[Column.PLEDGED.value] > 0]
    givers = df[(df[Column.PLEDGED.value] == 0) & (df[Column.GIVEN.value] > 0)]

    return pledged_givers, givers


def create_csv(title, df):
    try:
        cols = [
            Column.NAME.value,
            Column.SPOUSE.value,
            Column.AND_SPOUSE.value,
            Column.PLEDGED.value,
            Column.GIVEN.value,
            Column.EMAIL.value,
        ]
        df[cols].to_csv(title, index=False)
    except Exception as e:
        print(f"Failed to create CSV: {e}")


def main():
    try:
        df = pd.read_csv(input_file)
        formatted = format_couples(df)
        pledged_givers, givers = filter_pledgers_and_givers(formatted)
        create_csv("pledgedgivers.csv", pledged_givers)
        create_csv("givers.csv", givers)
    except FileNotFoundError:
        print("Error: {} file not found.".format(input_file))
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
