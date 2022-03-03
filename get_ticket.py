from jira import JIRA
from datetime import datetime
from calendar import monthrange

username="companyuser1"
api_token="password22."
jiraURL="https://jira.company.com/"

def main():

   options = {'server': jiraURL}
   jira = JIRA(options, basic_auth=(username, api_token))

   #PRD-9508 - Patching of the PRD Environments March 2021
   #PR0D_TIK-5470 - PROD Patching Ticket for April 2021
   #PR0D_TIK-5475 - PROD subtask
   issue = jira.issue('PRD-9736')

   print(issue)
   print("Issue Key: "+issue.key)
   print("Project Key: "+issue.fields.project.key)
   print("Project ID:"+issue.fields.project.id)
   print("IssueType Id:"+issue.fields.issuetype.id)
   print("Reporter:"+str(issue.fields.reporter))
   print("Summary:"+issue.fields.summary)
   print("Assigned:"+str(issue.fields.assignee))
   print("Description:"+issue.fields.description)
   print("Subtask:"+str(issue.fields.subtasks)) # for tid
   print("issuelinks:"+str(issue.fields.issuelinks)) # for oss
  # print("Parent Issue:"+str(issue.fields.parent))  # for subtask
   print("R&D-Project Related:"+str(issue.fields.customfield_12000))

#10408 for subtasks

def test():
   envs = ["DEVOPS", "DEV", "CORE", "DEMO", "PROD", "QA"]
   role_dict = {"comLinuxAdmUser1": "Linux",
                "comWinAdmUser1": "Windows"}
   for x in role_dict:
      for env in envs:
         summary = "PROD " + str(role_dict[x]) + " Patching " + env + " Environment"
         print(summary)


def last_day_of_month(date_value):
   return date_value.replace(day=monthrange(date_value.year, date_value.month)[1])


if __name__== "__main__" :
     main()
     #test()

     #given_date = datetime.now().date()
     #print(last_day_of_month(given_date))

