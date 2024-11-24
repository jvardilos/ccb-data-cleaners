import pandas as pd
from enum import Enum

input_file = "womens-retreat.csv"


class Column(Enum):
    FULL_NAME = "Profile Matched to"
    FIRST_NAME = "First Name"
    LAST_NAME = "Last Name"
    EMAIL = "Email"
    PHONE = "Mobile Phone"
    DOUBLE = "Choose Your Lodging Option: Double Occupancy"
    BUNK = "Choose Your Lodging Option: Bunkhouse Lodging"
    ACCOMODATION = "Lodging Option"


def split_signups(df):

    bunk = df[df[Column.BUNK.value] == 1].copy()
    bunk[Column.ACCOMODATION.value] = "Bunkhouse Lodging"

    double = df[df[Column.DOUBLE.value] == 1].copy()
    double[Column.ACCOMODATION.value] = "Double Occupancy"

    return bunk, double


def create_csv(title, df):
    try:
        cols = [
            Column.FULL_NAME.value,
            Column.FIRST_NAME.value,
            Column.LAST_NAME.value,
            Column.EMAIL.value,
            Column.PHONE.value,
            Column.ACCOMODATION.value,
        ]
        df[cols].to_csv(title, index=False)
    except Exception as e:
        print(f"Failed to create CSV: {e}")


def main():
    try:
        df = pd.read_csv(input_file)
        bunk, double = split_signups(df)
        create_csv("retreat-signups-bunkhouse.csv", bunk)
        create_csv("retreat-signups-double-occupancy.csv", double)
    except FileNotFoundError:
        print("Error: {} file not found.".format(input_file))
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
