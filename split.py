import pandas as pd

givings_file = "givings.csv"
families_file = "families.csv"


class Column:
    FAMILY = "Family"
    FAMILY_ID = "Family ID"
    REPLACED_NAME = "Primary Contact and Spouse"
    PRIMARY = "Primary"
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


def convert_to_dollar(df):
    df[Column.PLEDGED] = df[Column.PLEDGED].apply(lambda x: f"${x}")
    df[Column.GIVEN] = df[Column.GIVEN].apply(lambda x: f"${x}")

    return df


def filter_pledgers_and_givers(df):
    pledged_givers = df[df[Column.PLEDGED] > 0].copy()
    givers = df[(df[Column.PLEDGED] == 0) & (df[Column.GIVEN] > 0)].copy()

    dollar_pledged_givers = convert_to_dollar(pledged_givers)
    dollar_givers = convert_to_dollar(givers)

    return dollar_pledged_givers, dollar_givers


def filter_pledgers(pledgers):
    # TODO: make this split by new vs old pledgers
    return pledgers, pledgers


# do we want these givers to include children's giving?
def breakdowns(givings, families):

    # replace/new column of names of primary/spouse by family id found in families list
    contacts = givings.merge(
        families[[Column.FAMILY_ID, Column.REPLACED_NAME]],
        on=Column.FAMILY_ID,
        how="left",
    )

    # clean names and addresses
    contacts[[Column.PRIMARY, Column.SPOUSE, Column.AND_SPOUSE]] = contacts[
        Column.REPLACED_NAME
    ].apply(clean_names)
    contacts = clean_address(contacts)

    # make the splits
    pledgers, givers = filter_pledgers_and_givers(contacts)
    year_1, year_2 = filter_pledgers(pledgers)

    # 5. return them
    return year_1, year_2, givers


def create_csv(title, df):
    try:
        cols = [
            Column.FAMILY,
            Column.PRIMARY,
            Column.SPOUSE,
            Column.AND_SPOUSE,
            Column.PLEDGED,
            Column.GIVEN,
            Column.EMAIL,
            Column.ADDRESS,
        ]
        df[cols].to_csv(title, index=False)
    except Exception as e:
        print(f"Failed to create CSV: {e}")


def main():
    try:
        givings = pd.read_csv(givings_file)
        families = pd.read_csv(families_file)
        pledged_1_year, pledged_2_years, givers = breakdowns(givings, families)
        create_csv("1_year.csv", pledged_1_year)
        create_csv("2_years.csv", pledged_2_years)
        create_csv("givers.csv", givers)
    except FileNotFoundError:
        print("Error: {} or {} not found.".format(givings, families))
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
