from enum import Enum


class Column(Enum):
    NAME = "Name(s)"
    FAMILY = "Family"
    LAST_NAME = "Last Name"
    FIRST_NAME = "First Name"
    SPOUSE = "Spouse"
    AND_SPOUSE = "Spouse2"
    PLEDGED = "Total Pledged"
    EMAIL = "Email"
    START_DATE = "Start"


cols = [
    # for debugging
    Column.NAME.value,
    Column.FAMILY.value,
    Column.FIRST_NAME.value,
    # Only add "and spouse"
    Column.AND_SPOUSE.value,
    Column.SPOUSE.value,
    Column.PLEDGED.value,
    Column.EMAIL.value,
    # for debugging
    Column.START_DATE.value,
    "name_list",
    "new_pledge",
]


def create_csv(title, df):
    try:
        df[cols].to_csv(title, index=False)
    except Exception as e:
        print(f"Failed to create CSV: {e}")


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


def clean_names(name_string):
    # Split the string by commas and strip any whitespace
    parts = [x.strip() for x in name_string.split(",")]
    if len(parts) == 4:
        # Format the string as: "lastname1, name1 & name2"
        return f"{parts[0].strip()}, {parts[1].strip()} & {parts[3].strip()}"
    return name_string  # return original if format is unexpected
