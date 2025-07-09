# import gspread
# from google.oauth2.service_account import Credentials

# SERVICE_ACCOUNT_FILE = 'streamlit-userauth-d2f6ec3db520.json'

# SCOPES = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]


# credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# gc = gspread.authorize(credentials)

# sh = gc.open("users data")
# worksheet = sh.sheet1

# worksheet.append_row(["Test", "test@example.com", "hashedpassword", "2025-07-09T12:00:00"])
# print("Row added successfully!")
