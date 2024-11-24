import pandas as pd
from enum import Enum

input_file = "pledge_and_giving_detail.csv"


class Column(Enum):
    NAME = "Name(s)"
    LAST_NAME = "Last Name"
    FIRST_NAME = "First Name"
    SPOUSE = "Spouse"
    AND_SPOUSE = "Spouse2"
    PLEDGED = "Total Pledged"
    GIVEN = "Total Given (all-time)"
    EMAIL = "Email"
    STREET = "Street"
    CITY = "City"
    STATE = "State"
    POSTAL = "Postal Code"
    ADDRESS = "Address"


def format_address(df):
    # Combine street, city, state, and postal code into a single address string
    df[Column.ADDRESS.value] = (
        df[Column.STREET.value]
        + ", "
        + df[Column.CITY.value]
        + ", "
        + df[Column.STATE.value]
        + " "
        + df[Column.POSTAL.value]
    )

    return df


def clean_names(name_string):
    # Split the string by commas and strip any whitespace
    parts = [x.strip() for x in name_string.split(",")]
    if len(parts) == 4:
        # Format the string as: "lastname1, name1 & name2"
        return f"{parts[0].strip()}, {parts[1].strip()} & {parts[3].strip()}"
    return name_string  # return original if format is unexpected


def format_couples(df):
    # clean up name data
    df[Column.NAME.value] = df[Column.NAME.value].apply(clean_names)
    # Last name column
    df[Column.LAST_NAME.value] = df[Column.NAME.value].str.extract(r"^(\w+),?")[0]
    # First name column
    df[Column.FIRST_NAME.value] = df[Column.NAME.value].str.extract(r",\s*([\w]+)")[0]

    # Handling the spouse name by detecting patterns with '&' or additional commas
    df[Column.SPOUSE.value] = (
        df[Column.NAME.value].str.extract(r"&\s*(\w+)|,\s*(\w+)$")[0].fillna("")
    )

    # Creating the 'AND_SPOUSE' column
    df[Column.AND_SPOUSE.value] = df[Column.SPOUSE.value].apply(
        lambda x: f" and {x}" if x else ""
    )

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
    try:
        cols = [
            Column.NAME.value,
            Column.LAST_NAME.value,
            Column.FIRST_NAME.value,
            Column.SPOUSE.value,
            Column.AND_SPOUSE.value,
            Column.PLEDGED.value,
            Column.GIVEN.value,
            Column.EMAIL.value,
            Column.ADDRESS.value,
        ]
        df[cols].to_csv(title, index=False)
    except Exception as e:
        print(f"Failed to create CSV: {e}")


def main():
    try:
        df = pd.read_csv(input_file)
        formatted_c = format_couples(df)
        formatted = format_address(formatted_c)
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
