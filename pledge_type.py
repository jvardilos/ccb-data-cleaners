import pandas as pd

from cleaning import create_csv, format_couples, Column

pledge_modification_family = "list_of_families.csv"
giving_detail = "fixed_pledge_and_giving_detail.csv"


def get_pledged(df):
    df[Column.PLEDGED.value] = df.apply(
        lambda row: (
            row["new_pledge"]
            if row[Column.PLEDGED.value] == 0 and pd.notnull(row["new_pledge"])
            else row[Column.PLEDGED.value]
        ),
        axis=1,
    )
    dfp = df[df[Column.PLEDGED.value] > 0].copy()
    print(dfp[Column.PLEDGED.value].sum())

    dfp[Column.PLEDGED.value] = dfp[Column.PLEDGED.value].apply(lambda x: f"${x}")
    return dfp


# we determined that start date is a good value for when a new person pledges
def get_new_pledger(df):
    new = df[df[Column.START_DATE.value] == "2024-12-01"].copy()
    df_new_rm = df[~df.isin(new.to_dict(orient="list")).all(axis=1)]
    return new, df_new_rm


def handle_modification_pledger(mod, df):
    dfm = df[df["Family"].isin(mod["Family"])]
    remove = df[~df.isin(dfm.to_dict(orient="list")).all(axis=1)]
    return dfm, remove


def main():
    try:
        mod_list = pd.read_csv(pledge_modification_family)
        gd = pd.read_csv(giving_detail)
        p = get_pledged(gd)
        p = format_couples(p)

        create_csv("TESTING.csv", p)

        new, df_new_rm = get_new_pledger(p)
        mod, no_change = handle_modification_pledger(mod_list, df_new_rm)

        create_csv("new-pledgers.csv", new)
        create_csv("modified-pledgers.csv", mod)
        create_csv("no-change-pledgers.csv", no_change)
    except FileNotFoundError:
        if pledge_modification_family == "":
            print("Error: {} file not found.".format(pledge_modification_family))
        elif giving_detail == "":
            print("Error: {} file not found.".format(giving_detail))
    except pd.errors.EmptyDataError:
        print("Error: No data in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
