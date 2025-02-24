import pandas as pd
from config import Column, givings_file, families_file
from cleaning import clean_names, get_contacts, clean_address
from filters import (
    filter_pledgers,
    filter_pledgers_and_givers,
    filter_no_addresses,
    filter_no_emails,
    remove_non_members,
    rename_cols,
)


def breakdowns(givings, families):
    contacts = get_contacts(givings, families)
    contacts = rename_cols(contacts)

    # clean names and addresses
    contacts[[Column.NAME, Column.SPOUSE]] = contacts[Column.REPLACED_NAME].apply(
        clean_names
    )

    contacts = clean_address(contacts)

    contacts, non_members = remove_non_members(contacts)

    # make the splits
    no_email = filter_no_emails(contacts)
    no_address = filter_no_addresses(contacts)
    pledgers, givers = filter_pledgers_and_givers(contacts)
    half, full = filter_pledgers(pledgers)

    return half, full, givers, no_address, no_email, non_members


def create_csv(title, df):
    try:
        cols = [
            Column.FAMILY,
            Column.NAME,
            Column.SPOUSE,
            Column.PLEDGED,
            Column.GIVEN,
            Column.EMAIL,
            Column.ADDRESS,
        ]
        df[cols].to_csv(title, encoding="utf-8-sig", index=False)
    except Exception as e:
        print(f"Failed to create CSV: {e}")


def main():
    try:
        givings = pd.read_csv(givings_file, encoding="utf-8-sig")
        families = pd.read_csv(families_file, encoding="utf-8-sig")
        fto_halfway, fto_full, givers, no_address, no_email, non_members = breakdowns(
            givings, families
        )
        create_csv("FTO_one_year_pledge.csv", fto_halfway)
        create_csv("FTO_two_year_pledge.csv", fto_full)
        create_csv("FTO_giving_no_pledge.csv", givers)
        create_csv("no_address.csv", no_address)
        create_csv("no_email.csv", no_email)
        create_csv("non_church_member_givings.csv", non_members)
    except FileNotFoundError:
        print("Error: {} or {} not found.".format(givings, families))
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
