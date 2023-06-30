from __future__ import annotations

##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
##You must also turn on the Google Sheets API in your Google Console:
##https://console.cloud.google.com/apis/library/browse?
## Add you IAM user as an editor to the Google Sheet
from __future__ import annotations
import pprint
from typing import List, Dict
from pydantic import BaseModel, Field
from googleapiclient.discovery import build



from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    GoogleSheetID: str = Field(
        ...,
        description='SheetId (from the URL) of your Google Sheet',
        title='GoogleSheetID',
    )
    range: str = Field(
        ...,
        description='The cell range you wish to read in from Google Sheets.',
        title='range',
    )








def gcp_read_google_sheets_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def gcp_read_google_sheets(
    handle,
    GoogleSheetID: str,
    range: str
    ) -> Dict:

    service = build('sheets', 'v4', credentials=handle)
    sheet  = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=GoogleSheetID,
        range=range
        ).execute()
    print("result",result)
    return result


