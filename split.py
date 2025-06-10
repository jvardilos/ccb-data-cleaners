import pandas as pd
import csv
from config import (
    Column,
    givings_file,
    families_file,
    exclude,
    one_year_file,
    two_year_file,
    giver_file,
    no_address_file,
    no_email_file,
)
from cleaning import clean_names, get_contacts, clean_address, full_names
from filters import (
    filter_pledgers,
    filter_pledgers_and_givers,
    filter_no_addresses,
    filter_no_emails,
    fix_non_members,
    rename_cols,
    fmt_families,
    join_family_name,
)


def breakdowns(givings, families):
    contacts = get_contacts(givings, families)
    contacts = rename_cols(contacts)
    contacts = clean_address(contacts)
    contacts[Column.NAME] = contacts[Column.REPLACED_NAME].apply(clean_names)
    contacts[Column.NAME] = contacts.apply(fix_non_members, axis=1)
    contacts[Column.FAMILY] = contacts[Column.THE_FAMILY].apply(fmt_families)
    contacts[Column.FULL_NAMES] = contacts.apply(join_family_name, axis=1)
    contacts = contacts[~contacts[Column.FULL_NAMES].isin(exclude)]
    contacts[Column.CONTACT] = full_names(contacts)

    # make the splits
    no_email = filter_no_emails(contacts)
    no_address = filter_no_addresses(contacts)
    pledgers, givers = filter_pledgers_and_givers(contacts)
    half, full = filter_pledgers(pledgers)

    return (
        half,
        full,
        givers,
        no_address,
        no_email,
    )


def create_csv(title, df):
    try:
        cols = [
            Column.FAMILY_ID,
            Column.CONTACT,
            Column.FAMILY,
            Column.NAME,
            Column.PLEDGED,
            Column.GIVEN,
            Column.EMAIL,
            Column.ADDRESS,
            Column.FULL_NAMES,
        ]
        df[cols].to_csv(
            title,
            encoding="utf-8-sig",
            index=False,
            quoting=csv.QUOTE_ALL,
            quotechar='"',
        )
    except Exception as e:
        print(f"Failed to create CSV: {e}")


def main():
    try:
        givings = pd.read_csv(givings_file, encoding="utf-8-sig")
        families = pd.read_csv(families_file, encoding="utf-8-sig")
        fto_halfway, fto_full, givers, no_address, no_email = breakdowns(
            givings, families
        )
        create_csv(one_year_file, fto_halfway)
        create_csv(two_year_file, fto_full)
        create_csv(giver_file, givers)
        create_csv(no_address_file, no_address)
        create_csv(no_email_file, no_email)
    except FileNotFoundError:
        print("Error: {} or {} not found.".format(givings, families))
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
