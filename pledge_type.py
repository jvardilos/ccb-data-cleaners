import pandas as pd

# from giving_breakdowns import clean_names
from enum import Enum

pledge_modification_family = "list_of_families.csv"
giving_detail = "pledge_and_giving_detail.csv"


class Column(Enum):
    NAME = "Name(s)"
    FAMILY = "Family"
    START_DATE = "Start"
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


cols = [
    # for debugging
    # Column.NAME.value,
    Column.FAMILY.value,
    Column.FIRST_NAME.value,
    # Only add "and spouse"
    Column.AND_SPOUSE.value,
    # Column.SPOUSE.value,
    Column.PLEDGED.value,
    Column.EMAIL.value,
    # for debugging
    # Column.START_DATE.value,
]


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


def get_pledged(df):
    dfp = df[df[Column.PLEDGED.value] > 0].copy()
    dfp[Column.PLEDGED.value] = dfp[Column.PLEDGED.value].apply(lambda x: f"${x}")
    return dfp


# we determined that start date is a good value for when a new person pledges
def get_new_pledger(df):
    new = df[df[Column.START_DATE.value] == "2024-12-01"].copy()
    return new


def handle_modification_pledger(mod, df):
    modded = mod.merge(df, how="inner", on="Family")
    return modded


def get_no_change(df, new, mod):
    # match columns
    df = df[cols]
    new = new[cols]
    mod = mod[cols]

    # remove new and modified pledgers
    remove = df[~df.isin(new.to_dict(orient="list")).all(axis=1)]
    remove = remove[~remove.isin(mod.to_dict(orient="list")).all(axis=1)]
    return remove


def create_csv(title, df):
    try:
        df[cols].to_csv(title, index=False)
    except Exception as e:
        print(f"Failed to create CSV: {e}")


def main():
    try:
        mod_list = pd.read_csv(pledge_modification_family)
        gd = pd.read_csv(giving_detail)
        p = get_pledged(gd)
        p = format_couples(p)

        create_csv("TESTING.csv", p)

        new = get_new_pledger(p)
        mod = handle_modification_pledger(mod_list, p)
        no_change = get_no_change(p, new, mod)

        create_csv("new-pledgers.csv", new)
        create_csv("modified-pledgers.csv", mod)
        create_csv("no-change-pledgers.csv", no_change)
    except FileNotFoundError:
        if pledge_modification_family == "":
            print("Error: {} file not found.".format(pledge_modification_family))
        elif giving_detail == "":
            print("Error: {} file not found.".format(giving_detail))
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
