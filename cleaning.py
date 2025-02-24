import pandas as pd
from config import Column


def get_contacts(givings, families):
    # replace/new column of names of primary/spouse by family id found in families list

    givings[Column.TEMP] = givings.groupby(Column.FAMILY_ID).cumcount()
    families[Column.TEMP] = families.groupby(Column.FAMILY_ID).cumcount()

    contacts = givings.merge(
        families[[Column.FAMILY_ID, Column.REPLACED_NAME, Column.TEMP]],
        on=[Column.FAMILY_ID, Column.TEMP],
        how="left",
    ).drop(columns=[Column.TEMP])

    return contacts


def clean_names(n):
    names = str(n).split(" & ")
    first_name = names[0]
    spouse = "and " + names[1] if len(names) > 1 else None
    return pd.Series([first_name, spouse])


def clean_address(df):
    # Combine street, city, state, and postal code into a single address string
    df[Column.ADDRESS] = (
        df[Column.STREET]
        + ", "
        + df[Column.CITY]
        + ", "
        + df[Column.STATE]
        + " "
        + df[Column.POSTAL]
    )

    return df
