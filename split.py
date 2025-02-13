import pandas as pd
from config import Column, givings_file, families_file
from cleaning import clean_names, clean_address
from filters import (
    filter_pledgers,
    filter_pledgers_and_givers,
    filter_no_addresses,
    filter_no_emails,
    remove_non_members,
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

    contacts, non_members = remove_non_members(contacts)

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
    non_members = rename_cols(non_members)

    return half, full, givers, no_address, no_email, non_members


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
