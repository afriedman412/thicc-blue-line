import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import boto3
from botocore.exceptions import NoCredentialsError

def download_google_sheet(SPREADSHEET_ID, RANGE_NAME):
    # Authenticate using the service account credentials
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = Credentials.from_service_account_file('nba_2019_2020_service_creds.json', scopes=SCOPES)

    # Build the service
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    cols = values[0]
    values = values[1:]
    print(cols)

    if not values:
        print('No data found.')
    else:
        df = pd.DataFrame(values, columns=cols)
        return df

def upload_to_s3(file_name, bucket, s3_key):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(file_name, bucket, s3_key)
        print(f'Successfully uploaded {file_name} to s3://{bucket}/{s3_key}')
    except FileNotFoundError:
        print('The file was not found')
    except NoCredentialsError:
        print('Credentials not available')


def process_budget_data(df, year="2024"):
    df['id'] = df.apply(
    lambda r: "_".join(
            [r['state'].lower(), r['city'].lower()]
        ).replace(" ", ""), 1
    )
    df['name'] = df.apply(
        lambda r: ", ".join(
            [r['city'].title(), r['state']]
        ), 1
    )
    df['budget_type'] = df.apply(
        lambda r: r['expense'].lower()[0] + str(r['year'])[-2:], 1
    )

    budget_df = df.query("year==@year & expense!='Education'")[['id', 'name', 'expense', 'year', 'budget']].set_index(['id', 'name']).pivot(
        columns='expense', values=['budget']
    )
    budget_df.columns = ['general_fund', 'police']
    budget_df.reset_index(inplace=True)

    budget_df['police'] = budget_df['police'].fillna('1')
    budget_df['general_fund'] = budget_df['general_fund'].fillna('5')
    return budget_df


def load_coords(coords_path='coordinate_df.csv'):
    coords = pd.read_csv(coords_path).query("use=='x'")
    coords['id'] = coords.apply(
        lambda r: "_".join(
            [r['state'].lower(), r['city'].lower()]
        ).replace(" ", ""), 1
    )
    return coords


def combine_data(coords, budget_df):
    big_df = pd.merge(coords, budget_df, on='id')
    for c in ['police', 'general_fund']:
        big_df[c] = big_df[c].map(lambda p: p.replace("$", "").replace(",", ""))

    city_locations_df = big_df.rename(
                columns={'x':'cx', 'y':'cy'}
            )[['id', 'name', 'cx', 'cy']].dropna()

    budget_data_df = big_df.rename(
                columns={'police':'policeBudget', 'general_fund':'totalBudget'}
            ).set_index('id')[['name', 'policeBudget', 'totalBudget']]
    return city_locations_df, budget_data_df