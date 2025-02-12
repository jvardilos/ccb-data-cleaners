from config import Column, year_1, year_2, pledge, given


def convert_to_dollar(df):
    df[Column.TOTAL_PLEDGED] = df[Column.TOTAL_PLEDGED].apply(lambda x: f"${x}")
    df[Column.GIVEN_ALL_TIME] = df[Column.GIVEN_ALL_TIME].apply(lambda x: f"${x}")

    return df


def filter_pledgers_and_givers(df):
    pledged_givers = df[df[Column.TOTAL_PLEDGED] > 0].copy()
    givers = df[
        (df[Column.TOTAL_PLEDGED] == 0) & (df[Column.GIVEN_ALL_TIME] > 0)
    ].copy()

    pg_sum = pledged_givers[Column.GIVEN_ALL_TIME].sum()
    g_sum = givers[Column.GIVEN_ALL_TIME].sum()
    print("pledged amount:          ", pg_sum)
    print("pledged amount deficit:         ", pg_sum - pledge)
    print("given amount:            ", g_sum)
    print("given amount deficit:           ", g_sum - given)
    print("total given (all time):  ", pg_sum + g_sum)
    print("total given original df: ", df[Column.GIVEN_ALL_TIME].sum())

    dollar_pledged_givers = convert_to_dollar(pledged_givers)
    dollar_givers = convert_to_dollar(givers)

    return dollar_pledged_givers, dollar_givers


def filter_pledgers(pledgers):

    full = pledgers[pledgers[Column.PLEDGED_TIME] == year_2]
    half = pledgers[pledgers[Column.PLEDGED_TIME] == year_1]

    return half, full


def rename_cols(df):
    return df.rename(
        columns={
            Column.GIVEN_ALL_TIME: Column.GIVEN,
            Column.TOTAL_PLEDGED: Column.PLEDGED,
        }
    )
