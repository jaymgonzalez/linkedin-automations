from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import pandas as pd
import gspread

# Define the scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# Add your JSON key file
creds = ServiceAccountCredentials.from_json_keyfile_name("auto-csv.json", scope)

# Authenticate with Google
client = gspread.authorize(creds)


# Open the Google Sheet
def sheet_to_df(sheet_name):
    sheet = client.open(sheet_name).worksheet(sheet_name)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    return df


def df_to_sheet(df, sheet_name, include_index=False, create_sheet=False):
    if create_sheet:
        rows, cols = df.shape
        sheet = client.open(sheet_name)
        sheet.add_worksheet(
            title=sheet_name + "-withMessage", rows=str(rows + 1), cols=str(cols)
        )
        set_with_dataframe(sheet, df, include_index=include_index)
    else:
        sheet = client.open(sheet_name).worksheet(sheet_name)
        set_with_dataframe(sheet, df, include_index=include_index)
