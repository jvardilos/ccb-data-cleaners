import pandas as pd
from enum import Enum

input_file = "pledge_and_giving_detail.csv"


class Column(Enum):
    NAME = "Name(s)"
    # SPOUSE = "Spouse"
    # AND_SPOUSE = "Spouse2"
    PLEDGED = "Total Pledged"
    GIVEN = "Total Given (all-time)"
    EMAIL = "Email"


# TODO: split names in (<last name>, <name1> & <name2>), (<last name1>, <name1>, <last name2>, <name2>)
# and (<last name>, <name>)
def format_couples(df):
    # df[[Column.NAME.value, Column.SPOUSE.value]] = df[Column.NAME.value].str.extract(
    #     r"(\w+)(?:\s*&\s*(\w+))?", expand=True
    # )
    # df[Column.AND_SPOUSE.value] = df[Column.SPOUSE.value].apply(
    #     lambda x: f"and {x}" if pd.notna(x) else ""
    # )

    return df


def filter_pledgers_and_givers(df):
    pledged_givers = df[df[Column.PLEDGED.value] > 0].copy()
    givers = df[(df[Column.PLEDGED.value] == 0) & (df[Column.GIVEN.value] > 0)].copy()

    dollar_pledged_givers = convert_to_dollar(pledged_givers)
    dollar_givers = convert_to_dollar(givers)

    return dollar_pledged_givers, dollar_givers


def convert_to_dollar(df):
    df[Column.PLEDGED.value] = df[Column.PLEDGED.value].apply(lambda x: f"${x}")
    df[Column.GIVEN.value] = df[Column.GIVEN.value].apply(lambda x: f"${x}")

    return df


def create_csv(title, df):
    # Name(s),First Name,First Name (Secondary),First Name (and prefix),Email,Total Pledged,Total Given (all-time)

    try:
        cols = [
            Column.NAME.value,
            # Column.SPOUSE.value,
            # Column.AND_SPOUSE.value,
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
        create_csv("FTO-pledge-givers.csv", pledged_givers)
        create_csv("FTO-no-pledge-givers.csv", givers)
    except FileNotFoundError:
        print("Error: {} file not found.".format(input_file))
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
