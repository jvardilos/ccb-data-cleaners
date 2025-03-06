import pandas as pd

from split import create_csv
from config import Column, one_year_file, two_year_file, giver_file


def switch_full_names(name):

    names = str(name).split(" and ")

    first_name = names[0]
    second_name = str(names[1]).split(" ")[0]

    return second_name + " and " + first_name


def nameswitch(row):
    family = row[Column.FULL_NAMES]
    split_name = str(row[Column.NAME]).split(" and ")

    if len(split_name) > 1:
        print()
        switch_prompt = (
            input("family {}, Do you want to switch these names? (Y/n):".format(family))
            .strip()
            .lower()
        )

        if switch_prompt == "y" or switch_prompt == "":
            row[Column.NAME] = split_name[1] + " and " + split_name[0]
            full_name = switch_full_names(family) + " " + row[Column.FAMILY]
            row[Column.FULL_NAMES] = full_name

            print()
            print("switched {}".format(row[Column.FULL_NAMES]))

    return row


def switching(one_year: pd.DataFrame, two_year, giver):
    one_year = one_year.apply(nameswitch, axis=1)
    two_year = two_year.apply(nameswitch, axis=1)
    giver = giver.apply(nameswitch, axis=1)
    return one_year, two_year, giver


def main():
    try:
        one_year = pd.read_csv(one_year_file, encoding="utf-8-sig")
        two_year = pd.read_csv(two_year_file, encoding="utf-8-sig")
        giver = pd.read_csv(giver_file, encoding="utf-8-sig")

        fto_halfway, fto_full, givers = switching(one_year, two_year, giver)

        create_csv(one_year_file, fto_halfway)
        create_csv(two_year_file, fto_full)
        create_csv(giver_file, givers)
    except FileNotFoundError:
        print(
            "Error: {}, {}, or {} not found.".format(
                one_year_file, two_year_file, giver_file
            )
        )
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
