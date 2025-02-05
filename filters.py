from config import Column, year_1, year_2


def convert_to_dollar(df):
    df[Column.PLEDGED] = df[Column.PLEDGED].apply(lambda x: f"${x}")
    df[Column.GIVEN] = df[Column.GIVEN].apply(lambda x: f"${x}")

    return df


def filter_pledgers_and_givers(df):
    pledged_givers = df[df[Column.PLEDGED] > 0].copy()
    givers = df[(df[Column.PLEDGED] == 0) & (df[Column.GIVEN] > 0)].copy()

    dollar_pledged_givers = convert_to_dollar(pledged_givers)
    dollar_givers = convert_to_dollar(givers)

    return dollar_pledged_givers, dollar_givers


def filter_pledgers(pledgers):

    full = pledgers[pledgers[Column.PLEDGED_TIME] == year_2]
    half = pledgers[pledgers[Column.PLEDGED_TIME] == year_1]

    return half, full
