import pandas as pd
import json
from data_prep_helpers import download_google_sheet, upload_to_s3, process_budget_data, load_coords, combine_data
from dotenv import load_dotenv

year = '2024'

SPREADSHEET_ID = '1SqS5Xc7UrbuYiRY6Rcx3MYzDu7BXihvcclJjKQdWOCg'
RANGE_NAME = 'annotations_reformed!A1:F99999'
BUCKET_NAME = 'thicc-blue-bucket'

load_dotenv()

print('getting budget data...')
df = download_google_sheet(SPREADSHEET_ID, RANGE_NAME)

print('processing data...')
budget_df = process_budget_data(df)
coords_df = load_coords()
city_locations_df, budget_data_df = combine_data(coords_df, budget_df)
with open("city_locations.json", "w+") as f:
    json.dump(
        city_locations_df.dropna().to_dict('records'), f)
    
with open("budget_data.json", "w+") as f:
    json.dump(
        budget_data_df.dropna().to_dict('index'), f
    )

for j in ['city_locations', 'budget_data']:
    j += '.json'
    print(f'uploading {j}...')
    upload_to_s3(j, BUCKET_NAME, j)

print("MISSING DATA:")
print(budget_data_df[budget_data_df['policeBudget'].map(float) < 2]['name'])