import pandas as pd
from config import Column


def clean_names(n):
    names = str(n).split(" & ")
    primary = names[0]
    spouse = names[1] if len(names) > 1 else None
    and_spouse = " and " + names[1] if len(names) > 1 else None
    return pd.Series([primary, spouse, and_spouse])


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
