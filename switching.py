import pandas as pd

from split import create_csv
from config import one_year_file, two_year_file, giver_file


def nameswitch(df):
    print(df)
    return df


def switching(one_year, two_year, giver):
    one_year = nameswitch(one_year)
    two_year = nameswitch(two_year)
    giver = nameswitch(giver)
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
