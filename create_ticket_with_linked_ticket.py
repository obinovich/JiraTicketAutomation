from jira import JIRA
from datetime import datetime
from calendar import monthrange
import getpass
import requests
import json

# Jira AUthentication Credentials
username="companyuser1"
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
def create_ticket(key, summary, description, issuetype_id):
    issue_dict = {
        'project': {'key':key},
        'summary': summary,
        'description': description,
        'issuetype': {'id': issuetype_id},
        'customfield_12000': {'id':'12301'}, # "customfield_12000":"Invalid value 'N' passed for customfield 'R&D-Project Related'. Allowed values are: 12300[Y], 12301[N], -1"
    }
    new_issue = jira.create_issue(fields=issue_dict)
    update_ticket(new_issue)

    return new_issue
    #print(new_main_issue.key)

# update single ticket with assignee
def update_ticket(issue):
    issue_dict = {
        'assignee': {'name': 'comuser2'},
    }

    issue.update(fields=issue_dict)
    print(issue.key+" is updated with assignee")

# create multiple tickets
def create_multiple_ticket(in_issue):
    key = "COPS"
    issuetype_id = "10702"  # "COPS Request"
    description = in_issue.fields.description
    envs = [ "PRD", "QA", "DR", "SBX"] # exclude UAT, "DEV"

    for env in envs:
        summary = env + " - PRD Patching Ticket for " + period
        link_issue=create_ticket(key, summary, description, issuetype_id)
        print(link_issue.key+" is created.")

        jira.create_issue_link(type='is cloned by', inwardIssue=in_issue.key, outwardIssue=link_issue.key, comment=None)
        print(summary+" ("+link_issue.key+") is linked to "+ in_issue.key)

# Get last day of the month.
def last_day_of_month(date_value):
   return date_value.replace(day=monthrange(date_value.year, date_value.month)[1])

#Create entry on monday.com under Security patching of servers
#
def create_monday_entry(tdate, ticketkey, summary):
    apiKey = "eywfgyefefhihe774394594hhn437g632g"
    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": apiKey}

    query5 = 'mutation ($myItemName: String!, $columnVals: JSON!) { create_item (board_id:1967000031, group_id:new_group57174 ,item_name:$myItemName, column_values:$columnVals) { id } }'
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
    #create primary issue using info from 'COPS-9508'
    issue_prev = jira.issue('PRD-9508')
    key = "PRD"
    issuetype_id = "100702"  # "PRD key Request ID"
    description = issue_prev.fields.description
    summary = "PRD Patching Ticket for " + period

    parentIssue = create_ticket(key, summary, description, issuetype_id)
    print("Primary issue "+parentIssue.key+" is created.")

    # for existing ticket
    #pry_issue = jira.issue('PRD-10005')

    monthEnd = last_day_of_month(now)
    create_monday_entry(monthEnd, parentIssue.key, summary)

    # create ticket links for Parent ticket
    create_multiple_ticket(parentIssue)


if __name__== "__main__" :
    main()
