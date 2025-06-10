givings_file = "givings.csv"
families_file = "families.csv"
one_year_file = "FTO_one_year_pledge.csv"
two_year_file = "FTO_two_year_pledge.csv"
giver_file = "FTO_giving_no_pledge.csv"
no_address_file = "no_address.csv"
no_email_file = "no_email.csv"

year_1 = "2024-12-01"
year_2 = "2023-12-01"

pledge = 0
given = 0

# Fill list with names you wish to exclude
exclude = []


class Column:
    CONTACT = "Contact"
    NAME = "First Name"
    FAMILY = "Family"
    FAMILY_ID = "Family ID"
    REPLACED_NAME = "Primary Contact and Spouse"
    PRIMARY = "Name(s)"
    TRIMMED = "Trimmed"
    TEMP = "Temp"
    TOTAL_PLEDGED = "Total Pledged"
    PLEDGED = "Pledge"
    PLEDGED_TIME = "Start"
    GIVEN_ALL_TIME = "Total Given (report date range)"
    GIVEN = "Given"
    EMAIL = "Email"
    STREET = "Street"
    CITY = "City"
    STATE = "State"
    POSTAL = "Postal Code"
    ADDRESS = "Address"
    MOBILE_PHONE = "Mobile Phone"
    HOME_PHONE = "Home Phone"
    WORK_PHONE = "Work Phone"
    THE_FAMILY = "The <Family> Family"
    FULL_NAMES = "Full Names"
