from config import Column, year_1, year_2, pledge, given


def convert_to_dollar(df):
    df[Column.PLEDGED] = df[Column.PLEDGED].apply(lambda x: f"${x}")
    df[Column.GIVEN] = df[Column.GIVEN].apply(lambda x: f"${x}")

    return df


def filter_pledgers_and_givers(df):
    pledged_givers = df[df[Column.PLEDGED] > 0].copy()
    givers = df[(df[Column.PLEDGED] == 0) & (df[Column.GIVEN] > 0)].copy()

    pg_sum = pledged_givers[Column.GIVEN].sum()
    g_sum = givers[Column.GIVEN].sum()
    print("pledged amount:         ", pg_sum)
    print("pledged amount deficit:         ", pg_sum - pledge)
    print("given amount:           ", g_sum)
    print("given amount deficit:           ", g_sum - given)
    print("total given (all time): ", pg_sum + g_sum)
    print("total given og df:      ", df[Column.GIVEN].sum())

    dollar_pledged_givers = convert_to_dollar(pledged_givers)
    dollar_givers = convert_to_dollar(givers)

    return dollar_pledged_givers, dollar_givers


def filter_pledgers(pledgers):

    full = pledgers[pledgers[Column.PLEDGED_TIME] == year_2]
    half = pledgers[pledgers[Column.PLEDGED_TIME] == year_1]

    return half, full
