from jira import JIRA
from datetime import datetime
from calendar import monthrange
import getpass
import requests
import json

# Jira AUthentication Credentials
username="companyuser"
api_token=getpass.getpass(prompt='Enter Password:')
#api_token=""
jiraURL="https://jira.company.com/"
#jiraURL="https://jira-sandbox.company.com/"     #test environment
options = {'server': jiraURL}

# Jira AUthentication
try:
    jira = JIRA(options, basic_auth=(username, api_token))
except:
    print("incorrect password")

# Date objects to ticket summary
now = datetime.now().date()
period = now.strftime("%B %Y")

# create single ticket
def create_ticket(key, summary, description, issuetype_id, assignee):
    issue_dict = {
        'project': {'key':key},
        'summary': summary,
        'description': description,
        'issuetype': {'id': issuetype_id},
        'assignee': {'name': assignee},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    #print(new_issue.key)
    return new_issue

# create subtasks in tickets
def create_subtask(key,parentIssue):
    issuetype_id = "10408"  # "subtasks"
    description = "Task for deploying all OS patches from Linux in the DEVOPS environment. \n" \
                  "To be closed when finished. "

    envs = ["DEVOPS", "DEV","CORE", "DEMO (SANDBOX)", "PROD"]
    role_dict = {"comLinuxAdmUser1":"Linux",
                 "comWinAdmUser1":"Windows"}

    for env in envs:
        for x in role_dict:
            
            if (env=="PUSH" and x=="comWinAdmUser1"):
                continue    #skip for push windows environment
                
            summary = "PRD " + str(role_dict[x]) + " Patching " + env + " Environment"
            assignee = x
            issue_dict = {
                'project': {'key':key},
                'summary': summary,
                'description': description,
                'issuetype': {'id': issuetype_id},
                'assignee': {'name': assignee},
                'parent': {'key':parentIssue.key},
            }
            new_issue = jira.create_issue(fields=issue_dict)
            print("Subtask ("+new_issue.key+" - "+summary+" has been created)")

# Get last day of the month.
def last_day_of_month(date_value):
   return date_value.replace(day=monthrange(date_value.year, date_value.month)[1])

#Create entry on monday.com under Security patching of servers
# SCC - TID platform and solution = 179060533
def create_monday_entry(tdate, ticketkey,summary):
    apiKey = "###your API key####"
    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": apiKey}

    query5 = 'mutation ($myItemName: String!, $columnVals: JSON!) { create_item (board_id:100000033, group_id:topics ,item_name:$myItemName, column_values:$columnVals) { id } }'
    vars = {
        'myItemName': summary,
        'columnVals': json.dumps({
            'link': {'text': ticketkey, 'url': 'https://jira.company.com/browse/' + ticketkey},
            'status': {'label': 'To Start'},
            'date': {'date': str(tdate)}
        })
    }

    data = {'query': query5, 'variables': vars}
    r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
    print(r.json())


def main():
    #create Parent ticket from previous ticket TIDDO-5470
    issue_prev = jira.issue('PRD_TIK-5470')
    key = "PRD_TIK"
    issuetype_id = "11601"  # "PRD_TIK Request ID"
    description = issue_prev.fields.description
    summary = "PRD Patching Ticket for " + period
    assignee = "comLinuxAdmUser1"
    parentIssue = create_ticket(key, summary, description, issuetype_id, assignee)
    print("Primary issue " + parentIssue.key + " is created.")
    
    monthEnd = last_day_of_month(now)
    create_monday_entry(monthEnd,parentIssue.key,summary)

    # create subtasks for Parent ticket
    create_subtask(key,parentIssue)


if __name__== "__main__" :
    main()

