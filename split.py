import pandas as pd
from config import Column, givings_file, families_file
from cleaning import clean_names, clean_address
from filters import (
    filter_pledgers,
    filter_pledgers_and_givers,
    filter_no_addresses,
    filter_no_emails,
    rename_cols,
)


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
    families = clean_address(families)

    # Fill missing addresses in contacts with those from families
    contacts[Column.ADDRESS] = contacts[Column.ADDRESS].fillna(
        contacts[Column.FAMILY_ID].map(
            families.set_index(Column.FAMILY_ID)[Column.ADDRESS]
        )
    )

    print(families[Column.ADDRESS])

    # make the splits
    no_email = filter_no_emails(contacts)
    no_address = filter_no_addresses(contacts)
    pledgers, givers = filter_pledgers_and_givers(contacts)
    half, full = filter_pledgers(pledgers)

    half = rename_cols(half)
    full = rename_cols(full)
    givers = rename_cols(givers)
    no_address = rename_cols(no_address)
    no_email = rename_cols(no_email)

    return half, full, givers, no_address, no_email


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
            Column.HOME_PHONE,
            Column.MOBILE_PHONE,
            Column.WORK_PHONE,
        ]
        df[cols].to_csv(title, index=False)
    except Exception as e:
        print(f"Failed to create CSV: {e}")


def main():
    try:
        givings = pd.read_csv(givings_file)
        families = pd.read_csv(families_file)
        fto_halfway, fto_full, givers, no_address, no_email = breakdowns(
            givings, families
        )
        create_csv("fto_halfway.csv", fto_halfway)
        create_csv("fto_full.csv", fto_full)
        create_csv("givers.csv", givers)
        create_csv("no_address.csv", no_address)
        create_csv("no_email.csv", no_email)
    except FileNotFoundError:
        print("Error: {} or {} not found.".format(givings, families))
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
