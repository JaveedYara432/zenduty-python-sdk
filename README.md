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
        self.team_member_id = <unique_id of a team_member> # Random member id. 
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
            team_id = <unique_id of a team>, # UUID, which is unique_id of the team
            first_name="John",
            last_name="doe",
            role=3,
            email=test_email,
        )
```
#### PATCH - Update Account Member
```python
update_account_member = self.account_member_client.update_account_member(
    account_member_username=<unique_id of a member>,
    first_name=test_first_name,
    last_name=f"Doe {random.randint(2,10000000000000000000000)}",
    role=2,
)
```
#### GET - Get Account member
#### Get details about a particular team member
````python
account_member = self.account_member_client.get_account_member(
            account_member_id=<unique_id of a member>
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
delete_account_member = self.account_member_client.delete_account_member(account_member_id=<unique_id of a member>)
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
            team_id=<unique_id of a team>
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
            team_id=<unique_id of a team>
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
                        "user": <unique_id of a user>,
                        "position": 1,
                    }
                ],
            }
        ]

        self.overrides = [
            {
                "name": "",
                "user": <unique_id of a user>,
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

#### POST - Create a Maintenance
````python
class SDKMaintenanceClient(SDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id=<unique_id of a team>
        )
        self.maintenance_client = self.teams_client.get_maintenance_client(
            self.team_by_id
        )
        self.maintenance_name = f"Maintenance Mode - {self.datetime_timestamp}"

    def create_maintenance(self):
        create_maintenance = self.maintenance_client.create_team_maintenance(
            name=self.maintenance_name,
            start_time="2026-07-08T18:06:00",
            end_time="2026-07-08T18:06:00",
            service_ids=[list<unique_id of services>],
        )
````
#### GET - Get all Maintenances
````python
get_maintenance_by_id = self.maintenance_client.get_maintenance_by_id(
            maintenance_id=<unique_id of a maintenance>
        )
````
#### PATCH - Update a Maintenance
````python
update_maintenance = self.maintenance_client.update_maintenance(
            maintenance_id=<unique_id of a maintenance>,
            name="Updated Maintenance Name",
            start_time="2026-07-08T18:06:00",
            end_time="2026-07-08T18:06:00",
            service_ids=[list<unique_id of services>],
        )
````
#### DEL - Delete a Maintenance
````python
delete_maintenance = self.maintenance_client.delete_maintenance(
            maintenance_id=unique_id of a maintenance>
        )
````

## Incidents
What is an Incident??

An incident on Zenduty is an event that is not part of usual operations, and that disrupts operational processes within a Service that is owned by a team. Incidents can be automatically created by an alert integration within the service or manually by a user.

An incident on Zenduty has three states:

Triggered: Triggered is the first state of the incident. Zenduty will continue escalating the alert, depending on the escalation policy, as long as the incident is in the Triggered state.
Acknowledged: When an incident is acknowledged by a user, Zenduty stops all further escalations.
Resolved: Marking an incident as resolved implies that the incident has been remediated. Incidents can be resolved automatically by the service integration that created it, or manually by a user.

#### POST - Create an Incident
````python
class SDKIncidentsClient(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.incident_client = IncidentClient(client=self.client)
        self.incident_name = f"Incident - {self.datetime_timestamp}"
        self.incident_notes = f"Incident Notes - {self.datetime_timestamp}"
        self.incident_tags = f"Incident Tags - {self.datetime_timestamp}"

    def create_incident(self):
        create_incident = self.incident_client.create_incident(
            title=self.incident_name, service=<unique_id of a service>
        )

````
#### POST - Create an Incident Note
````python
    self.note_client = self.incident_client.get_note_client(
        incident_id=<unique_id of a incident>
    )

    # Creating an incident note, attaching it to an incident
    create_incident_note = self.note_client.create_incident_note(
        note=self.incident_notes
    )
````
#### GET - Get all Incident Notes
````python
get_all_incident_notes = self.note_client.get_all_incident_notes()
````
#### GET - Get Incident note by id
````python
 get_incident_note_by_id = self.note_client.get_incident_note_by_id(
            incident_note_unique_id=<unique_id of a incident note>
        )
````
#### PATCH - Update an Incident note
````python
update_incident_note = self.note_client.update_incident_note(
            incident_note_unique_id=<unique_id of a incident note>,
            note="Updated Incident Note",
        )
````
#### DEL - Delete an Incident note
````python
 delete_incident_note = self.note_client.delete_incident_note(
            incident_note_unique_id=<unique_id of a incident note>
        )
````
#### POST - Create an Incident Tag
````python
        self.tag_client = self.incident_client.get_tags_client(<incident_number of an incident>)

        create_incident_tag = self.tag_client.create_tag(
            team_tag=<incident_number of an incident>
        )
````
#### GET - Get all Incident Tags
````python
get_all_tags = self.tag_client.get_all_tags()
```` 
#### GET - Get all Incidents
````python
get_all_incidents = self.incident_client.get_all_incidents(page=1)
````
#### GET - Get Alerts of Incidents
````python
get_alerts_by_incident = self.incident_client.get_alerts_for_incident(
            incident_number<sincident_number of an incident>
        )
````
#### PATCH - Update an Incident
````python
update_incident = self.incident_client.update_incident(
            incident_id=<unique_id of an incident>,
            title="Updated Incident Name",
            status=3,
            service="a91a3a00-8de9-472c-ad2e-61e7c89db062",
        )
````

## Postmortem
#### POST - Create a Postmortem
````python
class SDKPostMortemClient(TestSDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.incident_name = "blahblah"
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id=<unique_id of a team>
        )
        self.incident_client = IncidentClient(client=self.client)
        self.incident_name = f"Incident - {self.datetime_timestamp}"
        self.postmortem_client = self.teams_client.get_postmortem_client(
            self.team_by_id
        )
        self.postmortem_name = f"Postmortem - {self.datetime_timestamp}"

    def create_postmortem(self):
        # Create the Incident
        create_incident = self.incident_client.create_incident(
            title=self.incident_name, service=<unique_id of a service>
        )

        # Create the Postmortem
        create_postmortem = self.postmortem_client.create_postmortem(
            author=<unique_id of the user who made the postmortem>,
            incidents=[list<unique_id of the incident>],
            title="Test Postmortem",
        )

````
#### GET - Get postmortem by id
````python
self.postmortem_by_id = self.postmortem_client.get_postmortem_by_id(
            postmortem_id=<unique_id of a postmortem>
        )
```` 
#### PATCH - Update a postmortem
````python
pdate_postmortem = self.postmortem_client.update_postmortem(
            <unique_id of a postmortem>,
            author=<unique_id of the user who made the postmortem>,
            incidents=[list<unique_id of a service>],
            title="Test Postmortem Updated",
        )
````
#### DEL - Delete a postmortem
````python
delete_postmortem = self.postmortem_client.delete_postmortem(
            <unique_id of a postmortem>
        )
````

## Priorities
#### POST - Create a priority
````python
class SDKPrioritiesClient(SDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id=<unique_id of a team>
        )
        self.priority_client = self.teams_client.get_priority_client(self.team_by_id)
        self.priority_name = f"Priority - {self.datetime_timestamp}"

    def create_priority(self):
        create_priority = self.priority_client.create_priority(
            name=self.priority_name,
            description="Priority Description",
            color="red",
        )

````
#### GET - Get all priorities
````python
get_all_priorities = self.priority_client.get_all_priorities()
````
#### GET - Get priorities by ID
````python
self.priority_by_id = self.priority_client.get_priority_by_id(
            priority_id=<unique_id of a priority>
        )
````
#### PATCH - Update the priority
````python
update_priority = self.priority_client.update_priority(
            <unique_id of a priority>,
            name="Test Priority Updated",
            description="Test Priority",
        )
````
#### DEL - Delete a priority
````python
delete_priority = self.priority_client.delete_priority(<unique_id of a priority>)
```` 

## Roles
#### POST - Create a Role
````python
class SDKRolesClient(SDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id=<unique_id of a team>
        )
        self.role_client = self.teams_client.get_incident_role_client(self.team_by_id)
        self.role_name = f"Role - {self.datetime_timestamp}"

    def create_role(self):
        self.create_role = self.role_client.create_incident_role(
            title="Test Role",
            description="Test Role",
            rank=1,
        )
````
#### GET - Get incident role by id
````python
 self.get_role_by_id = self.role_client.get_incident_role_by_id(
            role_id=<unique_id of an incident role>
        )
````
#### PATCH - Update an incident role
````python
self.update_role = self.role_client.update_incident_role(
            role=<unique_id of an incident role>,
            title="Test Role Updated",
        )
```` 
#### DEL - Delete an incident role
````python
self.delete_role = self.role_client.delete_incident_role(
            role=<unique_id of an incident role>
        )
````

## Services
#### POST - Create a Service
````python
class SDKServicesClient(SDKTeamsClient):
    def __init__(self):
        super().__init__()
        # Making the Teams Client
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        # Making the Service Client
        self.service_client = self.teams_client.get_service_client(self.team_ids[0])
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id=<unique_id of a team>
        )
        self.escalation_policy_client = self.teams_client.get_escalation_policy_client(
            self.team_by_id
        )
        self.priority_client = self.teams_client.get_priority_client(self.team_by_id)
        self.sla_client = self.teams_client.get_sla_client(self.team_by_id)
        # Making the names
        self.ep_name = f"EP - {self.datetime_timestamp}"
        self.priority_name = f"Priority - {self.datetime_timestamp}"
        self.sla_name = f"SLA - {self.datetime_timestamp}"
        self.service_name = f"Service - {self.datetime_timestamp}"

    def test_create_service(self):
        # Create the escalation policy
        self.rule_build = [
            {
                "delay": 0,
                "targets": [
                    {"target_type": 2, "target_id": <unique_id of a user who has to be in the esp>}
                ],
                "position": 1,
            }
        ]
        create_escalation_policy = self.escalation_policy_client.create_esp(
            self.ep_name, rules=self.rule_build
        )


        # Create the Priority
        create_priority = self.priority_client.create_priority(
            name=self.priority_name,
            description="Priority Description",
            color="red",
        )

        # Create the SLA
        create_sla = self.sla_client.create_sla(name="Test SLA", escalations=[])

        # Finally create the service
        create_service = self.service_client.create_service(
            name=f"Test Service - {self.datetime_timestamp}",
            escalation_policy=<unique_id of an esp>,
            team_priority=<unique_id of a team priority>,
            sla=<unique_id of an SLA>,
        )
````

## Integrations
#### POST - Create an integration
````python
integration_client = service_client.get_integration_client(svc=<unique_id of a service>)

create_integration = integration_client.create_intg( name="Test Integration", summary="Test Integration", application=<unique_id of an application>)

````
#### GET - Get all integrations
````python
all_integrations = integration_client.get_all_integrations()
````
#### GET - Get integration by id
````python
integration_by_id = integration_client.get_intg_by_id(intg=<unique_id of an integration>)
````
#### PATCH - Update an integration
````python
update_integration = integration_client.update_intg(intg=<unique_id of an integration>, name="Test Integration Updated", application=<unique_id of an application>)
````
#### DEL - Delete an integration
````python
delete_integration = integration_client.delete_intg(intg=<unique_id of an integration>)
````

## SLA
#### POST - Create an SLA
````python
sla_client = team_client.get_sla_client(team_by_id)
create_sla = sla_client.create_sla(name="Test SLA", escalations=[])
````
#### GET - Get SLA by id
````python
sla_by_id = sla_client.get_sla_by_id(sla_id=<unique_id of SLA>)
````
#### PATCH - Update SLA
````python
update_sla = sla_client.update_sla(sla=<unique_id of SLA>, name="Test SLA Updated", escalations=[])
````
#### DEL - Delete SLA
````python
delete_sla sla_client.delete_sla(sla=<unique_id of SLA>)
````

## Tags
#### POST - Create a tag
````python
tag_client = team_client.get_tag_client(team_by_id)
create_tag = tag_client.create_tag(name="TestXsadasd", color="red")
````
#### GET - Get all tags
````python
get_all_tags = tag_client.get_all_tags()
````
#### GET - GET tag by id
````python
get_tag = tag_client.get_tag_by_id(tags_id = <unique_id of a tag>)
````
#### PATCH - Update tag by id
````python
update_tag = tag_client(tag = <unique_id of a tag>, name="updated name", color="green")
````
#### DEL - Delete tag
````python
delete_tag = tag_client(tag = <unique_id of a tag>)
````


## Task templates
#### POST - Create a task template
````python
task_template_client = team_client.get_task_template_client(team_by_id)
create_task_template = task_template_client.create_task_template(
    name="Test Task Template", summary="Test Task Template"
)
````
#### GET - Get all task templates
````python
get_all_task_templates = task_template_client.get_all_task_template()
```` 
#### GET - Get task templates by id
````python
get_task_template_by_id =  task_template_client.get_task_template_by_id(
    task_template_id=<unique_id of a task template>
)
````
#### PATCH - Update the task template
````python
update_task_template = task_template_client.update_task_template(
    task_template = <unique_id of a task template>, name="Test Task Template Updated"
)
````
#### DEL - Delete the task template
````python
delete_task_template = task_template_client.delete_task_template(task_template = <unique_id of a task template>)
````



# Running tests

There is a sample skeleton code in tests/. Add your access token to it and modify the object and function name for testing purposes.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
