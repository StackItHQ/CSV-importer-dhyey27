import chunk as chunk
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Step 1: Set up Google Sheets API and create a client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('csvimporter-2723-7e83d5059d57.json', scope)
client = gspread.authorize(creds)

# Step 2: Open the Google Sheet
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1lVCR7KtAhG3OCJy-TSOD632Um5NA2l3Lm5sVDWdMn0g/edit?usp=sharing')
# Step 3: Get the worksheet object
worksheet = sheet.worksheet('Sheet1')

# Step 4: Read the CSV file in chunks and filter the columns
chunksize = 50000000000000000 # size of chunks depends on your available memory
filtered_columns = ['1', '3']  # Replace with your column names

# Prompt the user to choose whether to append the data to the existing sheet or create a new sheet
append_or_create = input("Do you want to append the data to the existing sheet or create a new sheet? (a/c): ")

# If the user chooses to append the data to the existing sheet, append the data
# If the user chooses to append the data to the existing sheet, append the data
if append_or_create == "a":
    data_to_append = []
    for chunk in pd.read_csv('SampleCSVFile_119kb.csv', chunksize=chunksize):
        filtered_chunk = chunk[filtered_columns]
        data_to_append.extend(filtered_chunk.values.tolist())
    worksheet.append_rows(data_to_append)
    print("Data imported successfully to Google Sheets!")

# If the user chooses to create a new sheet, create a new sheet and append the data
elif append_or_create == "c":
    new_worksheet = sheet.add_worksheet('New2 Sheet',rows=1000,cols=20)
    data_to_append = []
    for chunk in pd.read_csv('SampleCSVFile_119kb.csv', chunksize=chunksize):
        filtered_chunk = chunk[filtered_columns]
        data_to_append.extend(filtered_chunk.values.tolist())
    new_worksheet.append_rows(data_to_append)
    print("Data imported successfully to a new sheet in Google Sheets!")
