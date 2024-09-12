import pandas as pd
from enum import Enum


class column(Enum):
    NAME = "Name"
    SPOUSE = "Spouse"
    AND_SPOUSE = "Spouse2"
    PLEDGED = "Pledged"
    GIVEN = "Given"
    EMAIL = "Email"


def format_couples(df):
    df[[column.NAME.value, column.SPOUSE.value]] = df[column.NAME.value].str.extract(
        r"(\w+)(?:\s*&\s*(\w+))?", expand=True
    )
    df[column.AND_SPOUSE.value] = "and " + df[column.SPOUSE.value]
    return df


def filter_pledgers_and_givers(df):
    pledged_givers = df[df[column.PLEDGED.value] > 0]
    givers = df[(df[column.PLEDGED.value] == 0) & (df[column.GIVEN.value] > 0)]
    return pledged_givers, givers


def create_csv(title, df):
    cols = [
        column.NAME.value,
        column.SPOUSE.value,
        column.AND_SPOUSE.value,
        column.PLEDGED.value,
        column.GIVEN.value,
        column.EMAIL.value,
    ]
    df[cols].to_csv(title, index=False)


def main():
    df = pd.read_csv("sample.csv")

    formatted = format_couples(df)
    pledged_givers, givers = filter_pledgers_and_givers(formatted)
    create_csv("pledgedgivers.csv", pledged_givers)
    create_csv("givers.csv", givers)


if __name__ == "__main__":
    main()
