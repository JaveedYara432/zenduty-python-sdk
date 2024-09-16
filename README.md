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

Global Event Router is a webhook, when sent requests to it, would navigate it to a particular integration, to a particular request, if matched with the alert rules defined, would raise an alert.

Refer to this, for more information, https://apidocs.zenduty.com/#tag/Global-Router.

#### POST - Create Router
````python
class SDKGERClients(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.router_client = RouterClient(client=self.client)
        self.router_name = f"Router - {self.datetime_timestamp}"

    def create_router(self):
        create_router = self.router_client.create_router(
            name=self.router_name,
            description="Router Description",
        )
````
#### GET - List Routers
````python
list_router = self.router_client.get_all_routers()
````
#### GET - Get Router by ID
````python
find_router = self.router_client.get_router_by_id(router_id=<unique_id of a router>)
````
#### PATCH - Update a particular Router
````python
update_router = self.router_client.update_router(
    <unique_id of a router>,
    name="Updated Router Name",
    description="Updated Router Description",
)
````
#### DEL - Delete a particular Router
````python
delete_router = self.router_client.delete_router(<unique_id of a router>)
````

## Events
This object represents the events of an integration.

#### POST - Create an Event
````python
class SDKEventsClient(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.event_client = EventClient(client=self.client)
        self.event_name = f"Event - {self.datetime_timestamp}"

    def get_router_client(self):
        get_router = self.event_client.get_router_client()

    def test_create_event(self):
        create_event = self.event_client.create_event(
            integration_key=<unique_id of an Integration>,
            alert_type="info",
            message="This is info alert",
            summary="This is the incident summary111",
            entity_id=123455,
            payload={
                "status": "ACME Payments are failing",
                "severity": "1",
                "project": "kubeprod",
            },
            urls=[
                {
                    "link_url": "https://www.example.com/alerts/12345/",
                    "link_text": "Alert URL",
                }
            ],
        )

````

## Escalation Policy
Escalation policies dictate how an incident created within a service escalates within your team.

#### POST - Create an Escalation Policy
````python
class SDKEscalationPolicyClient(SDKTeamsClient):
    # Inheriting a few methods from the Teams Object.
    def __init__(self):
        super().__init__()
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.account_member_client = AccountMemberClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id="<unique_id of a team>"
        )
        self.escalation_policy_client = self.teams_client.get_escalation_policy_client(
            self.team_by_id
        )
        self.ep_name = f"EP - {self.datetime_timestamp}"

    def create_escalation_policy(self):

        self.rule_build = [
            {
                "delay": 0,
                "targets": [
                    {"target_type": 2, "target_id": "3544118d-fbf5-41e5-ae6c-5"}
                ],
                "position": 1,
            }
        ]
        create_escalation_policy = self.escalation_policy_client.create_esp(
            self.ep_name, rules=self.rule_build
        )

````
#### GET - Get Escalation Policies by ID
````python
self.escalation_policy_client.get_esp_by_id(
    esp_id=<unique_id of an escalation policy>
)
````
#### POST - Update Escalation Policy
````python
update_esp = self.escalation_policy_client.update_esp(
            esp=<unique_id of an escalation policy>,
            name="Test Updated",
            rules=self.rule_build,
        )
````
#### GET - Get all the escalation policies
````python
all_esp = self.escalation_policy_client.get_all_policies()
````
#### DEL - Delete an Escalation Policy
````python
delete_esp = self.escalation_policy_client.delete_esp(esp=<unique_id of an escalation policy>)
````

## Schedules
#### POST - Create an Escalation Policy
````python
class SDKSchedulesClient(SDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id="<unique_id of a team>"
        )
        self.schedules_client = self.teams_client.get_schedule_client(self.team_by_id)
        self.schedules_name = f"Schedules - {self.datetime_timestamp}"
        self.layers = [
            {
                "name": "Layer 1",
                "is_active": True,
                "restriction_type": 0,
                "restrictions": [],
                "rotation_start_time": "2025-07-29T03:30:00.000Z",
                "rotation_end_time": None,
                "shift_length": 86400,
                "users": [
                    {
                        "user": "<unique_id of a user>",
                        "position": 1,
                    }
                ],
            }
        ]

        self.overrides = [
            {
                "name": "",
                "user": "<unique_id of a user>",
                "start_time": "2024-07-29T11:54:34.745000Z",
                "end_time": "2024-07-29T18:29:59.999000Z",
            }
        ]

    def create_schedule(self):
        create_schedule = self.schedules_client.create_schedule(
            name=self.schedules_name,
            timezone="Asia/Kolkata",
            layers=self.layers,
            overrides=self.overrides,
        )

````
#### GET - Get all Schedules
````python
get_all_schedules = self.schedules_client.get_all_schedules()
````
#### GET - Get Schedules by ID
````python
self.get_schedule_by_id = self.schedules_client.get_schedule_by_id(
            schedule_id=<unique_id of a schedule>
        )
````
#### POST - Update a Schedule
````python
update_schedule = self.schedules_client.update_schedule(
            schedule=<unique_id of a schedule>,
            name="Test Schedule Updated",
        )
````
#### DEL - Delete a Schedule
````python
delete_schedule = self.schedules_client.delete_schedule(
            schedule=<unique_id of a schedule>
        )
````

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
