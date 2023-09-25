from datetime import datetime, timedelta
from pydantic import BaseModel
import jira

# Pydantic input schema

class JiraInput(BaseModel):
 handle: jira.client
 days: int

# Function to find JIRA issues older than a specified number of days
# Input: input_data - JIRA input data
# Output: List of JIRA issues

def find_older_jira_issues(input_data: JiraInput) -> List[str]:
 handle = input_data.handle
 days = input_data.days

 today = datetime.now().date()
 cutoff_date = today - timedelta(days=days)
 jql_query = f"createdDate <= '{cutoff_date}'"

 issues = handle.search_issues(jql_query)
 older_issues = [issue.key for issue in issues]

 return older_issues
