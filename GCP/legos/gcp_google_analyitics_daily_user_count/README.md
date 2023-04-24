[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]
(https://unskript.com/assets/favicon.png)
<h1>GCP Google Analytics Daily User Count</h1>

## Description
For a Given Google Analytics Account, extract the daily unique users for a give set of days.

## Lego Details
	gcp_google_analyitics_daily_user_count(handle, days:float, view_id:str)
		handle: Object of type unSkript GCP Connector.

	View_id: is the View ID of your Google Analytics account.
	Days: number of days of data to return.
	
	
	Note: For this Action to work, you must do a few things on the Google Side.
	The Google Credential used at unSkript has a service email (probably ending in 'iam.gserviceaccount.com'). 
	You'll need to add this email account as a user in your Google Analytics Account.

## Lego Input
This Lego takes inputs handle, View_id (string) and days (number).

## Lego Output
The Output is a Dictionary with keys of day (YYYYMMDD) and value of unique users for that day.

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)