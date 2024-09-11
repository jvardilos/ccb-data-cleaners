import pandas as pd

df = pd.read_csv('sample.csv')

name = 'Name'
spouse = 'Spouse'
andSpouse = 'Spouse2'
pledged = "Pledged"
given = 'Given'
email = 'Email'


# extract names of couples into columns
df[[name, spouse]] = df[name].str.extract(r'(\w+)(?:\s*&\s*(\w+))?', expand=True)
df[andSpouse] = 'and ' + df[spouse]


allgivers = df[df[given] > 0]

pledgedgivers = allgivers[allgivers[pledged] > 0]
givers = allgivers[allgivers[pledged] == 0]


# TODO: Strip all unecessary columns

cols = [name, spouse, andSpouse, pledged, given, email]
pledgedgivers[cols].to_csv('pledgedgivers.csv', index=False)
givers[cols].to_csv('givers.csv', index=False)