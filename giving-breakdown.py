import pandas as pd

df = pd.read_csv("sample.csv")

name = "Name"
spouse = "Spouse"
andSpouse = "Spouse2"
pledged = "Pledged"
given = "Given"
email = "Email"

# extract names of couples into columns
df[[name, spouse]] = df[name].str.extract(r"(\w+)(?:\s*&\s*(\w+))?", expand=True)
df[andSpouse] = "and " + df[spouse]

# TODO: do we want to include pledgers who have not given??
# split the dataset to those who have pledged and those who
# have given
pledgedgivers = df[df[pledged] > 0]
givers = df[(df["Pledged"] == 0) & (df["Given"] > 0)]

# create csv
cols = [name, spouse, andSpouse, pledged, given, email]
pledgedgivers[cols].to_csv("pledgedgivers.csv", index=False)
givers[cols].to_csv("givers.csv", index=False)
