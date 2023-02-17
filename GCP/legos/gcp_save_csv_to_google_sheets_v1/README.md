[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Save a CSV to a Google Sheet</h1>

## Description
This Action takes a variable CSV, and saves it to a Google Sheet

## Action Details

In order to run this Action, you'll need to:

1. Enable the Google Sheets API in yur GCP console (https://console.cloud.google.com/apis/library/browse?)
2. Add an IAM user as an editor of the Google Sheet.
3. Your "CSV" must have each line as an array.

```
def gcp_write_to_google_sheet(handle, csvList: List, GoogleSheetID: str, StartingCell: str) -> Dict:
    result = []

    service = build('sheets', 'v4', credentials=handle)
    sheet  = service.spreadsheets()
    body={'values':csvList}
    result = sheet.values().update(spreadsheetId=GoogleSheetID, range=StartingCell, valueInputOption='USER_ENTERED', body=body).execute()
    print("result",result)
   ```


## Action Input
csvList: CSV. Each line should be an array
GoogleSheetID: This is the ID of the Google Sheet the file will be saved into. You can get this from the URL of the sheet
StartingCell: Cell where the paste should begin


## Action Output
Dict of the inputs.  You will also see the Google Sheet update.

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)