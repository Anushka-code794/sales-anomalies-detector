import pandas as pd
from io import BytesIO

def read_google_sheet(sheet_url: str):
    if "/edit" in sheet_url:
        sheet_url = sheet_url.split("/edit")[0]
    csv_url = sheet_url + "/export?format=csv"
    df = pd.read_csv(csv_url)
    return df.to_dict(orient="records")

def parse_csv_file(file_bytes):
    df = pd.read_csv(BytesIO(file_bytes))
    return df.to_dict(orient="records")
 
