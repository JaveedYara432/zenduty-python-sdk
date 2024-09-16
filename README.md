# What is Zenduty??
Zenduty is a cutting edge platform for incident management. With high level automation, Zenduty enables faster and better incident resolution keeping developers first.

# Zenduty Python SDK

Python SDK to communicate with zenduty endpoints

## Installing

Installation can be done through pip, as follows:
```sh 
$ pip install zenduty-api
```
or you may grab the latest source code from GitHub: 
```sh
$ git clone https://github.com/Zenduty/zenduty-python-sdk
$ python3 setup.py install
```

## Contents
1) zenduty/api : contains the functions to communicate with zenduty API endpoints
2) zenduty/    : contains the common required files
3) bin/		   : contains sample script to run zenduty functions

## Getting started

Before you begin making use of the SDK, make sure you have your Zenduty Access Token.
You can then import the package into your python script.

First of all, start off by making a client which connects to Zenduty using API Token. And create a team, most of the operations we'd do start off by creating a team, and creating services. For now, we will start off with creating an instance of a team. 


The Approach here is to make clients here, every module will get a new client to make things simpler and easier for us to understand.


```python
import zenduty

class SDKTestingClient:
    def __init__(self):
        self.cred = ZendutyCredential("<ZENDUTY-API-TOKEN>")
        self.client = ZendutyClient(
            credential=self.cred, use_https=True
        )  # defaults to default service endpoint zenduty.com
```

It is important to note that each function returns a urllib3.response.HTTPResponse object.


## Teams
This object represents a team of the account. It lets you create different independent operational units in the account. You can check out the team docs here https://docs.zenduty.com/docs/teams.

A Team can have multiple Members, Services, Integrations, Schedules, Escalation Policies, Priorities, Maintenance, etc.. 


#### POST - Create a new team
````python
class SDKTeamsClient(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.teams_client = TeamsClient(client=self.client)
        self.team_member_id = "<unique_id of a team_member>" # Random member id. 
        self.invite_url = "https://zenduty.com/api/invite/accept/"
        self.test_team_name = f"Team - {self.datetime_timestamp}"

    def create_team(self):
        create_team = self.teams_client.create_team(self.test_team_name)
        return create_team
````

#### GET - List Teams
#### Will fetch all the teams present in that account
````python
list_teams = self.teams_client.list_teams()
````

#### PATCH - Update teams
#### Update the team 
````python
update_teams = self.teams_client.update_team(
            <unique_id of a team>, name="Updated Team Name"
        )
````

#### DEL - Delete team
````python
delete_teams = self.teams_client.delete_team(<unique_id of a team>)
````


## Account Member 
This object represents an account user. Each account member object has a role, which can be "owner," "admin," or "user." An account can have only one owner, but multiple admins and users.

Prerequisite: A team must be created, where the role of each member can be assigned.

#### GET - Invite a member to the team
#### Invite a member to the team.
```python
class SDKAccountMembersClient(SDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.teams_client = TeamsClient(client=self.client)
        self.account_member_client = AccountMemberClient(client=self.client)

    def account_members_invite(self):
        test_email = f"john.doe.{random.randint(2,10000000000000000000000)}@zenduty.com"
        
        account_member_invite = self.account_member_client.invite(
            team_id = "<unique_id of a team>", # UUID, which is unique_id of the team
            first_name="John",
            last_name="doe",
            role=3,
            email=test_email,
        )
```

#### PATCH - Update Account Member
```python
update_account_member = self.account_member_client.update_account_member(
    account_member_username="<unique_id Of a member>",
    first_name=test_first_name,
    last_name=f"Doe {random.randint(2,10000000000000000000000)}",
    role=2,
)
```

#### GET - Get Account member
#### Get details about a particular team member
````python
account_member = self.account_member_client.get_account_member(
            account_member_id="<unique_id Of a member>"
        )
````


#### GET - Get all the members of a team
#### Get details of all the members of the team.

````python
account_members = self.account_member_client.get_all_members()
````


#### DEL - Delete an Account member
#### Delete a particular member of the team.


````python
delete_account_member = self.account_member_client.delete_account_member(account_member_id="<unique_id Of a member>")
````


## Account Roles

#### POST - Create Account Role
#### There are a list of permissions you could give to a role. Please refer to these docs, https://apidocs.zenduty.com/#tag/Account-Custom-Role.

````python
class SDKAccountRolesClient(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.account_role_client = AccountRoleClient(client=self.client)

    def create_account_role(self):
        test_name = f"Account Role - {self.datetime_timestamp}"
        create_account_role = self.account_role_client.create_account_role(
            name=test_name,
            description="Account Role Description",
            permissions=["sla_read"],
        )
````
#### GET - Get an Account Role 
````python
get_account_role = self.account_role_client.get_account_role(
            account_role_id=<unique_id of the account_role>
        )
````
#### GET - Get a list of roles
````python
list_account_roles = self.account_role_client.list_account_roles()
````
#### PATCH - Update an Account Role
````python
test_name = f"Updated Account Role - {self.datetime_timestamp}"
        update_account_role = self.account_role_client.update_account_role(
            account_role_id=<unique_id of the account_role>,
            name=test_name,
            description="Updated Account Role Description",
            permissions=["sla_read"],
        )
````
#### DEL - Delete an Account Role
````python
delete_account_role = self.account_role_client.delete_account_role(
            account_role_id=<unique_id of the account_role>
        )
````

## Global Event Router
## Events
## Escalation Policy
## Schedules
## Maintenance
## Incidents
## Postmortem
## Priorities
## Roles
## Services
## Integrations
## SLA
## Tags
## Task templates



## Running tests

There is a sample skeleton code in bin/. Add your access token to it and modify the object and function name for testing purposes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
