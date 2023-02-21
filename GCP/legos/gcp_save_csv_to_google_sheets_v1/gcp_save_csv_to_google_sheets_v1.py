

##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
## CSV must have each line as a list. For Example:
##[['This file was created 02/17/2023'], 
##['Service Code', 'Quota Name', 'Quota Code', 'Quota Value', 'Quota Unit', 'Global?', 'Adjustable?'], 
##['AWSCloudMap', 'DiscoverInstances operation per account steady rate', 'L-514A639A', 1000.0, 'None', False, True], ['AWSCloudMap', 'DiscoverInstances operation per account burst rate', 'L-76CF203B', 2000.0, 'None', False, True], ['AWSCloudMap', 'Namespaces per Region', 'L-0FE3F50E', 50.0, 'None', False, True],

##You must also turn on the Google Sheets API in your Google Console:
##https://console.cloud.google.com/apis/library/browse?

## Add you IAM user as an editor to the Google Sheet


from pydantic import BaseModel, Field
import pprint
from typing import List, Optional
from googleapiclient.discovery import build
from __future__ import annotations



class InputSchema(BaseModel):
    GoogleSheetID: str = Field(
        '',
        description='SheetId (from the URL) of your Google Sheet',
        title='GoogleSheetID',
    )
    StartingCell: str = Field(
        '"A1"',
        description='Starting Cell for the data insertion into the sheet.',
        title='StartingCell',
    )
    csvList: List = Field(
        '',
        description='List of rows to be inserted into the Google Sheet',
        title='csvList',
    )

from beartype import beartype
@beartype
def gcp_save_csv_to_google_sheets_v1_printer(output):
    if output is None:
        return
    pprint(output)

@beartype
def gcp_save_csv_to_google_sheets_v1(handle, csvList: List, GoogleSheetID: str, StartingCell: str) -> Dict:

    service = build('sheets', 'v4', credentials=handle)
    sheet  = service.spreadsheets()
    body={'values':csvList}
    result = sheet.values().update(spreadsheetId=GoogleSheetID, range=StartingCell, valueInputOption='USER_ENTERED', body=body).execute()
    print("result",result)
    return result


