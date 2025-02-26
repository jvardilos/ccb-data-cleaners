from config import Column, year_1, year_2, pledge, given


def fix_non_members(cols):
    name = cols[Column.NAME]
    primary = cols[Column.PRIMARY]
    primary = str(primary).split(", ")[1].split(" & ")[0]

    if name == "nan":
        return primary

    return name


def convert_to_dollar(df):
    df[Column.PLEDGED] = df[Column.PLEDGED].apply(lambda x: f"${x}")
    df[Column.GIVEN] = df[Column.GIVEN].apply(lambda x: f"${x}")

    return df


def filter_no_addresses(df):
    no_addresses = df[df[Column.ADDRESS].isna()]

    return no_addresses


def filter_no_emails(df):
    no_emails = df[df[Column.EMAIL].isna()]

    return no_emails


def filter_pledgers_and_givers(df):
    pledged_givers = df[df[Column.PLEDGED] > 0].copy()
    givers = df[(df[Column.PLEDGED] == 0) & (df[Column.GIVEN] > 0)].copy()

    pg_sum = pledged_givers[Column.GIVEN].sum() * 100
    g_sum = givers[Column.GIVEN].sum() * 100

    if pledge and given != 0.0:
        print("pledged amount:          ", pg_sum)
        print("pledged amount deficit:         ", pg_sum - pledge)
        print("given amount:            ", g_sum)
        print("given amount deficit:           ", g_sum - given)
        print("total given (all time):  ", pg_sum + g_sum)
        print("total given original df: ", df[Column.GIVEN].sum())

    dollar_pledged_givers = convert_to_dollar(pledged_givers)
    dollar_givers = convert_to_dollar(givers)

    return dollar_pledged_givers, dollar_givers


def filter_pledgers(pledgers):

    full = pledgers[
        (pledgers[Column.PLEDGED_TIME] == year_2)
        | (pledgers[Column.PLEDGED_TIME] == "varies")
    ]
    half = pledgers[pledgers[Column.PLEDGED_TIME] == year_1]

    return half, full


def rename_cols(df):
    return df.rename(
        columns={
            Column.GIVEN_ALL_TIME: Column.GIVEN,
            Column.TOTAL_PLEDGED: Column.PLEDGED,
            Column.FAMILY: Column.THE_FAMILY,
        }
    )


def fmt_families(family):
    return str(family).split("The ")[1].split(" Family")[0]
