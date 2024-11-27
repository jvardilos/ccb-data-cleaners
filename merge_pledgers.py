import pandas as pd

from cleaning import create_csv, format_couples, Column


all_family = "family.csv"
all_individual = "individual.csv"


def get_family_name_list(fam):
    fam = format_couples(fam)

    fam["name_list"] = fam.apply(
        lambda row: [
            f"{row[Column.LAST_NAME.value]}, {row[Column.FIRST_NAME.value]}"
        ]  # Primary person
        + (
            [
                f"{row[Column.LAST_NAME.value]}, {row[Column.SPOUSE.value]}"
            ]  # Spouse if exists
            if pd.notna(row[Column.SPOUSE.value]) and row[Column.SPOUSE.value]
            else []
        ),
        axis=1,
    )


def merge(fam, people):
    get_family_name_list(fam)

    # Prepare data
    fam_exploded = fam.explode("name_list").reset_index()
    fam["new_pledge"] = 0.0

    # Match and update pledges
    for _, row in people.iterrows():
        match_idx = fam_exploded.loc[fam_exploded["name_list"] == row["Name"], "index"]
        if not match_idx.empty:
            fam.loc[match_idx.iloc[0], "new_pledge"] += row[Column.PLEDGED.value]

    return fam


def find_amount(df):

    # Filter rows where Column.PLEDGED.value and "new_pledge" differ
    mismatched_rows = df[
        (df[Column.PLEDGED.value] != df["new_pledge"])
        & (df[Column.SPOUSE.value].str.strip() != "")
    ]

    create_csv("babys_first_mismatch.csv", mismatched_rows)

    # Calculate the total "new_pledge" amount
    total_new_pledge = mismatched_rows["new_pledge"].sum()
    total_pledge = mismatched_rows[Column.PLEDGED.value].sum()

    # Print the total "new_pledge" amount
    print(f"Total 'new_pledge' amount: {total_new_pledge}")
    print(f"Total 'old pledge' amount: {total_pledge}")


def main():
    try:
        family = pd.read_csv(all_family)
        individual = pd.read_csv(all_individual)

        merged = merge(family, individual)

        find_amount(merged)

        create_csv("fixed_pledge_and_giving_detail.csv", merged)
    except FileNotFoundError:
        if family == "":
            print("Error: {} file not found.".format(family))
        elif individual == "":
            print("Error: {} file not found.".format(individual))
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
