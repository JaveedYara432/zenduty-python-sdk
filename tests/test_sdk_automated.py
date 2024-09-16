import sys
import uuid
import time
import pytest
import random
import string
import zenduty
from pathlib import Path
from datetime import datetime, timedelta

# Importing V2 Clients
from zenduty.apiV2.client import ZendutyClient

# Importing V2 Internal Clients
from zenduty.apiV2.teams import TeamsClient
from zenduty.apiV2.events import EventClient
from zenduty.apiV2.incidents import IncidentClient
from zenduty.apiV2.events.router import RouterClient
from zenduty.apiV2.incidents.notes import IncidentNoteClient
from zenduty.apiV2.incidents.tags import IncidentTagClient
from zenduty.apiV2.accounts.roles import AccountRoleClient
from zenduty.apiV2.accounts.members import AccountMemberClient
from zenduty.apiV2.teams.escalation_policies.rules import RuleBuilder
from zenduty.apiV2.teams.escalation_policies.targets import TargetBuilder
from zenduty.apiV2.authentication.zenduty_credential import ZendutyCredential


class SDKTestingClient:
    def __init__(self):
        self.cred = ZendutyCredential("e3464dbec1590e0c226685e156f40ed541c3b715")
        self.client = ZendutyClient(
            credential=self.cred, use_https=True
        )  # defaults to default service endpoint zenduty.com
        self.datetime_timestamp = self.datetime_timestamp()

    @staticmethod
    def datetime_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def generate_uuid() -> str:
        # generate a random UUID
        return str(uuid.uuid4())


@pytest.mark.teams
class TestSDKTeamsClient(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.team_ids = []
        self.team_members = []
        self.team_member_unique_id = []
        self.teams_client = TeamsClient(client=self.client)
        self.team_member_id = "773c69f5-78f2-42ca-b3d9-b"
        self.invite_url = "https://zenduty.com/api/invite/accept/"
        self.test_team_name = f"Team - {self.datetime_timestamp}"

    @staticmethod
    def create_team(self):
        create_team = self.teams_client.create_team(self.test_team_name)
        return create_team

    @staticmethod
    def delete_team(self):
        delete_team = self.teams_client.delete_team(self.team_ids[0])

    # Teams testing
    def test_create_team(self):
        # Team1 is the name of the team and that is the payload
        create_team = self.teams_client.create_team(self.test_team_name)
        self.team_ids.append(create_team)
        assert create_team.name == self.test_team_name
        time.sleep(2)

    def test_find_team_by_id(self):
        find_team = self.teams_client.find_team_by_id(self.team_ids[0].unique_id)
        assert find_team.unique_id == self.team_ids[0].unique_id
        time.sleep(2)

    def test_list_team_member(self):
        list_team_members = self.teams_client.list_team_members(self.team_ids[0])
        assert list_team_members[0].team == self.team_ids[0].unique_id
        time.sleep(2)

    def test_add_team_member(self):
        add_team_member = self.teams_client.add_team_member(
            self.team_ids[0], username=self.team_member_id
        )
        assert str(add_team_member.team) == str(self.team_ids[0].unique_id)
        time.sleep(2)

    def test_find_team_member(self):
        list_team_members = self.teams_client.list_team_members(self.team_ids[0])
        self.team_member_unique_id.append(list_team_members[1].unique_id)
        find_team_member = self.teams_client.find_team_member(
            self.team_ids[0], member_unique_id=self.team_member_unique_id[0]
        )
        assert str(find_team_member.unique_id) == str(self.team_member_unique_id[0])
        time.sleep(2)

    def test_update_team_member(self):
        update_team_member = self.teams_client.update_team_member(
            self.team_ids[0], member_id=self.team_member_unique_id[0], role=1
        )
        assert update_team_member.role == 1 and str(
            update_team_member.unique_id
        ) == str(self.team_member_unique_id[0])
        time.sleep(2)

    def test_delete_team_member(self):
        delete_team_member = self.teams_client.delete_team_member(
            self.team_ids[0], member_id=self.team_member_unique_id[0]
        )
        time.sleep(2)

    def test_fetch_team_permissions(self):
        team_permissions = self.teams_client.fetch_team_permissions(self.team_ids[0])

    def update_team_permissions(self):
        updated_team_permissions = self.teams_client.update_team_permissions(
            permissions=["service_read"], team=self.team_ids[0]
        )
        assert "service_read" in updated_team_permissions

    def test_update_teams(self):
        update_teams = self.teams_client.update_team(
            self.team_ids[0], name="Updated Team Name"
        )
        assert str(update_teams.name) == "Updated Team Name"

    def test_delete_teams(self):
        delete_teams = self.teams_client.delete_team(self.team_ids[0])


@pytest.mark.accountmembers
class TestSDKAccountMembersClient(TestSDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.team_ids = []
        self.account_member_ids = []
        self.teams_client = TeamsClient(client=self.client)
        self.account_member_client = AccountMemberClient(client=self.client)

    def test_account_members_invite(self):
        create_team = self.teams_client.create_team(
            name="Random Testing Team" + self.datetime_timestamp
        )
        self.team_ids.append(create_team.unique_id)

        test_email = f"john.doe.{random.randint(2,10000000000000000000000)}@zenduty.com"

        account_member_invite = self.account_member_client.invite(
            team_id=self.team_ids[0],
            first_name="John",
            last_name="doe",
            role=3,
            email=test_email,
        )
        self.account_member_ids.append(account_member_invite.user.username)
        assert account_member_invite.user.email == test_email

    def test_account_member_update(self):
        test_first_name = f"Jane {random.randint(2,10000000000000000000000)}"
        # updated the email
        update_account_member = self.account_member_client.update_account_member(
            account_member_username=self.account_member_ids[0],
            first_name=test_first_name,
            last_name=f"Doe {random.randint(2,10000000000000000000000)}",
            role=2,
        )

        assert update_account_member.user.first_name == test_first_name

    def test_get_account_member(self):
        account_member = self.account_member_client.get_account_member(
            account_member_id=self.account_member_ids[0]
        )
        assert account_member.user.username == self.account_member_ids[0]

    def test_get_all_account_members(self):
        account_members = self.account_member_client.get_all_members()

    def test_delete_account_member(self):
        delete_account_member = self.account_member_client.delete_account_member(
            account_member_id=self.account_member_ids[0]
        )


@pytest.mark.accountroles
class TestSDKAccountRolesClient(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.account_role_ids = []
        self.account_role_client = AccountRoleClient(client=self.client)

    def test_create_account_role(self):
        test_name = f"Account Role - {self.datetime_timestamp}"
        create_account_role = self.account_role_client.create_account_role(
            name=test_name,
            description="Account Role Description",
            permissions=["sla_read"],
        )

        self.account_role_ids.append(create_account_role.unique_id)

        assert create_account_role.name == test_name

        time.sleep(2)

    def test_get_account_role(self):
        get_account_role = self.account_role_client.get_account_role(
            account_role_id=self.account_role_ids[0]
        )

        assert str(get_account_role.unique_id) == str(self.account_role_ids[0])
        time.sleep(2)

    def test_list_account_roles(self):
        list_account_roles = self.account_role_client.list_account_roles()
        time.sleep(2)

    def test_update_account_role(self):
        test_name = f"Updated Account Role - {self.datetime_timestamp}"
        update_account_role = self.account_role_client.update_account_role(
            account_role_id=self.account_role_ids[0],
            name=test_name,
            description="Updated Account Role Description",
            permissions=["sla_read"],
        )
        assert update_account_role.name == test_name
        time.sleep(2)

    def test_delete_account_role(self):
        delete_account_role = self.account_role_client.delete_account_role(
            account_role_id=self.account_role_ids[0]
        )
        time.sleep(2)


@pytest.mark.GER
class TestSDKGERClients(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.router_ids = []
        self.router_client = RouterClient(client=self.client)
        self.router_name = f"Router - {self.datetime_timestamp}"

    def test_create_router(self):
        create_router = self.router_client.create_router(
            name=self.router_name,
            description="Router Description",
        )
        self.router_ids.append(create_router.unique_id)
        assert str(create_router.name) == f"Router - {self.datetime_timestamp}"
        time.sleep(2)

    def test_list_routers(self):
        list_router = self.router_client.get_all_routers()
        for router in list_router:
            if str(router.name) == f"Router - {self.datetime_timestamp}":
                assert str(router.name) == f"Router - {self.datetime_timestamp}"
                break
        time.sleep(2)

    def test_get_router_by_id(self):
        find_router = self.router_client.get_router_by_id(router_id=self.router_ids[0])
        assert str(find_router.unique_id) == str(self.router_ids[0])
        time.sleep(2)

    def test_update_router(self):
        update_router = self.router_client.update_router(
            self.router_ids[0],
            name="Updated Router Name",
            description="Updated Router Description",
        )
        assert str(update_router.name) == "Updated Router Name"

        time.sleep(2)

    def test_delete_router(self):
        delete_router = self.router_client.delete_router(self.router_ids[0])
        time.sleep(2)


@pytest.mark.events
class TestSDKEventsClient(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.event_ids = []
        self.event_client = EventClient(client=self.client)
        self.event_name = f"Event - {self.datetime_timestamp}"

    def test_get_router_client(self):
        get_router = self.event_client.get_router_client()

    def test_create_event(self):

        create_event = self.event_client.create_event(
            integration_key="f86e6ade-f987-4cfc-b047-9ce9ca794b41",
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

        assert (
            create_event.integration_object.integration_key
            == "f86e6ade-f987-4cfc-b047-9ce9ca794b41"
        )


@pytest.mark.escalationpolicy
class TestSDKEscalationPolicyClient(TestSDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.escalation_policy_ids = []
        self.account_member_ids = []
        self.team_ids = []
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.account_member_client = AccountMemberClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id="999a17ed-c7c3-4860-9024-d11c18fa5fa4"
        )
        self.escalation_policy_client = self.teams_client.get_escalation_policy_client(
            self.team_by_id
        )
        self.ep_name = f"EP - {self.datetime_timestamp}"

    @staticmethod
    def generate_uuid() -> str:
        return str(uuid.uuid4())

    def test_create_escalation_policy(self):

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

        # Appending the unique_id to the escalation_policy_ids list
        self.escalation_policy_ids.append(create_escalation_policy.unique_id)
        assert create_escalation_policy.name == self.ep_name
        time.sleep(2)

    def test_get_esp_by_id(self):
        self.get_esp_by_id = self.escalation_policy_client.get_esp_by_id(
            esp_id=self.escalation_policy_ids[0]
        )
        assert self.get_esp_by_id.name == self.ep_name
        time.sleep(2)

    def test_update_esp(self):
        update_esp = self.escalation_policy_client.update_esp(
            esp=self.get_esp_by_id,
            name="Test Updated",
            rules=self.rule_build,
        )

        assert update_esp.name == "Test Updated"
        time.sleep(2)

    def test_get_all_policies(self):
        all_esp = self.escalation_policy_client.get_all_policies()
        time.sleep(2)

    def test_delete_esp(self):
        delete_esp = self.escalation_policy_client.delete_esp(esp=self.get_esp_by_id)
        time.sleep(2)


@pytest.mark.maintenance
class TestSDKMaintenanceClient(TestSDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.maintenance_ids = []
        self.account_member_ids = []
        self.team_ids = []
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id="999a17ed-c7c3-4860-9024-d11c18fa5fa4"
        )
        self.maintenance_client = self.teams_client.get_maintenance_client(
            self.team_by_id
        )
        self.maintenance_name = f"Maintenance Mode - {self.datetime_timestamp}"

    def test_create_maintenance(self):
        create_maintenance = self.maintenance_client.create_team_maintenance(
            name=self.maintenance_name,
            start_time="2026-07-08T18:06:00",
            end_time="2026-07-08T18:06:00",
            service_ids=["a91a3a00-8de9-472c-ad2e-61e7c89db062"],
        )

        self.maintenance_ids.append(create_maintenance.unique_id)
        assert create_maintenance.name == self.maintenance_name
        time.sleep(2)

    def test_get_all_maintenance(self):
        get_all_maintenance = self.maintenance_client.get_all_maintenance()

        time.sleep(2)

    def test_get_maintenance_by_id(self):
        get_maintenance_by_id = self.maintenance_client.get_maintenance_by_id(
            maintenance_id=self.maintenance_ids[0]
        )

        time.sleep(2)

    def test_update_maintenance_by_id(self):
        update_maintenance = self.maintenance_client.update_maintenance(
            maintenance_id=self.maintenance_ids[0],
            name="Updated Maintenance Name",
            start_time="2026-07-08T18:06:00",
            end_time="2026-07-08T18:06:00",
            service_ids=["a91a3a00-8de9-472c-ad2e-61e7c89db062"],
        )

        time.sleep(2)

    def test_delete_maintenance(self):
        delete_maintenance = self.maintenance_client.delete_maintenance(
            maintenance_id=self.maintenance_ids[0]
        )

        time.sleep(2)


@pytest.mark.incidents
class TestSDKIncidentsClient(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.incident_ids = []
        self.incident_number = []
        self.incident_notes_list = []
        self.incident_tags_list = []
        self.incident_client = IncidentClient(client=self.client)
        self.incident_name = f"Incident - {self.datetime_timestamp}"
        self.incident_notes = f"Incident Notes - {self.datetime_timestamp}"
        self.incident_tags = f"Incident Tags - {self.datetime_timestamp}"

    def test_create_incident(self):
        create_incident = self.incident_client.create_incident(
            title=self.incident_name, service="a91a3a00-8de9-472c-ad2e-61e7c89db062"
        )

        assert (
            str(create_incident.title) == self.incident_name
            and str(create_incident.service) == "a91a3a00-8de9-472c-ad2e-61e7c89db062"
        )

        self.incident_ids.append(create_incident.unique_id)
        self.incident_number.append(create_incident.incident_number)
        time.sleep(2)

    # check here for incident notes and tags
    def test_create_incident_note(self):
        # Creating a Incident Note client
        self.note_client = self.incident_client.get_note_client(
            incident_id=self.incident_ids[0]
        )

        # Creating an incident note, attaching it to an incident
        create_incident_note = self.note_client.create_incident_note(
            note=self.incident_notes
        )
        self.incident_notes_list.append(create_incident_note.unique_id)

        assert str(create_incident_note.note) == self.incident_notes

        time.sleep(2)

    def test_get_all_incident_notes(self):
        get_all_incident_notes = self.note_client.get_all_incident_notes()
        time.sleep(2)

    def test_get_incident_note_by_id(self):
        get_incident_note_by_id = self.note_client.get_incident_note_by_id(
            incident_note_unique_id=self.incident_notes_list[0]
        )
        time.sleep(2)

    # get this checked tomorrow
    def test_update_incident_note(self):
        update_incident_note = self.note_client.update_incident_note(
            incident_note_unique_id=self.incident_notes_list[0],
            note="Updated Incident Note",
        )

    def test_delete_incident_note(self):
        delete_incident_note = self.note_client.delete_incident_note(
            incident_note_unique_id=self.incident_notes_list[0]
        )

    # get this checked tomorrow
    def test_create_incident_tag(self):
        self.tag_client = self.incident_client.get_tags_client(self.incident_number[0])

        create_incident_tag = self.tag_client.create_tag(
            team_tag=self.incident_number[0]
        )

    def test_get_all_tags(self):
        get_all_tags = self.tag_client.get_all_tags()

    def test_get_tag_by_id(self):
        get_tag_by_id = self.tag_client.get_tag_by_id(self.incident_tags[0])

    def test_delete_incident_tag(self):
        delete_incident_tag = self.tag_client.delete_tag(self.incident_tags[0])

    def test_get_all_incidents(self):
        get_all_incidents = self.incident_client.get_all_incidents(page=1)

        for incident in get_all_incidents:
            if str(incident["title"]) == self.incident_name:
                assert str(incident["title"]) == self.incident_name
                break
        time.sleep(2)

    def test_get_alerts_by_incident(self):
        get_alerts_by_incident = self.incident_client.get_alerts_for_incident(
            incident_number=self.incident_number[0]
        )
        time.sleep(2)

    def test_update_incident(self):
        update_incident = self.incident_client.update_incident(
            incident_id=self.incident_ids[0],
            title="Updated Incident Name",
            status=3,
            service="a91a3a00-8de9-472c-ad2e-61e7c89db062",
        )

        assert (
            int(update_incident.status) == 3
            and str(update_incident.title) == "Updated Incident Name"
            and str(update_incident.unique_id) == str(self.incident_ids[0])
            and str(update_incident.incident_number) == str(self.incident_number[0])
        )


@pytest.mark.postmortem
class TestSDKPostMortemClient(TestSDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.team_ids = []
        self.incident_ids = []
        self.postmortem_ids = []
        self.account_member_ids = []
        self.incident_name = "blahblah"
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id="999a17ed-c7c3-4860-9024-d11c18fa5fa4"
        )
        self.incident_client = IncidentClient(client=self.client)
        self.incident_name = f"Incident - {self.datetime_timestamp}"
        self.postmortem_client = self.teams_client.get_postmortem_client(
            self.team_by_id
        )
        self.postmortem_name = f"Postmortem - {self.datetime_timestamp}"

    def test_create_postmortem(self):
        # Create the Incident
        create_incident = self.incident_client.create_incident(
            title=self.incident_name, service="a91a3a00-8de9-472c-ad2e-61e7c89db062"
        )

        # Create the Postmortem
        create_postmortem = self.postmortem_client.create_postmortem(
            author="3544118d-fbf5-41e5-ae6c-5",
            incidents=[create_incident.unique_id],
            title="Test Postmortem",
        )

        # Appending the unique id to the postmortem list.
        self.postmortem_ids.append(create_postmortem.unique_id)
        self.incident_ids.append(create_incident.unique_id)

    def test_get_postmortem_by_id(self):
        self.postmortem_by_id = self.postmortem_client.get_postmortem_by_id(
            postmortem_id=self.postmortem_ids[0]
        )

        assert self.postmortem_by_id.title == "Test Postmortem"

    def test_update_postmortem(self):
        update_postmortem = self.postmortem_client.update_postmortem(
            self.postmortem_by_id,
            author="3544118d-fbf5-41e5-ae6c-5",
            incidents=[self.incident_ids[0]],
            title="Test Postmortem Updated",
        )
        assert update_postmortem.title == "Test Postmortem Updated"

    def test_delete_postmortem(self):
        delete_postmortem = self.postmortem_client.delete_postmortem(
            self.postmortem_by_id
        )

        # Resolve the incident
        resolve_incident = self.incident_client.update_incident(
            incident_id=self.incident_ids[0],
            title=self.incident_name,
            status=3,
        )


@pytest.mark.priorities
class TestSDKPrioritiesClient(TestSDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.team_ids = []
        self.priority_ids = []
        self.account_member_ids = []
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id="999a17ed-c7c3-4860-9024-d11c18fa5fa4"
        )
        self.priority_client = self.teams_client.get_priority_client(self.team_by_id)
        self.priority_name = f"Priority - {self.datetime_timestamp}"

    def test_create_priority(self):
        create_priority = self.priority_client.create_priority(
            name=self.priority_name,
            description="Priority Description",
            color="red",
        )

        self.priority_ids.append(create_priority.unique_id)
        assert create_priority.name == self.priority_name
        time.sleep(2)

    def test_get_all_priorities(self):
        get_all_priorities = self.priority_client.get_all_priorities()
        time.sleep(2)

    def test_get_priority_by_id(self):
        self.priority_by_id = self.priority_client.get_priority_by_id(
            priority_id=self.priority_ids[0]
        )

        assert self.priority_by_id.name == self.priority_name

    def test_update_priority(self):
        update_priority = self.priority_client.update_priority(
            self.priority_by_id,
            name="Test Priority Updated",
            description="Test Priority",
        )

        assert update_priority.name == "Test Priority Updated"
        time.sleep(2)

    def test_delete_priority(self):
        delete_priority = self.priority_client.delete_priority(self.priority_ids[0])
        time.sleep(2)


@pytest.mark.roles
class TestSDKRolesClient(TestSDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.team_ids = []
        self.role_ids = []
        self.account_member_ids = []
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id="999a17ed-c7c3-4860-9024-d11c18fa5fa4"
        )
        self.role_client = self.teams_client.get_incident_role_client(self.team_by_id)
        self.role_name = f"Role - {self.datetime_timestamp}"

    def test_create_role(self):
        self.create_role = self.role_client.create_incident_role(
            title="Test Role",
            description="Test Role",
            rank=1,
        )

        self.role_ids.append(self.create_role.unique_id)
        assert self.create_role.title == "Test Role"
        time.sleep(2)

    def test_get_incident_role_by_id(self):
        self.get_role_by_id = self.role_client.get_incident_role_by_id(
            role_id=self.role_ids[0]
        )
        assert self.get_role_by_id.title == "Test Role"
        time.sleep(2)

    def test_update_incident_role(self):
        self.update_role = self.role_client.update_incident_role(
            role=self.get_role_by_id,
            title="Test Role Updated",
        )
        assert self.update_role.title == "Test Role Updated"
        time.sleep(2)

    def test_delete_incident_role(self):
        self.delete_role = self.role_client.delete_incident_role(
            role=self.get_role_by_id
        )
        time.sleep(2)


@pytest.mark.schedules
class TestSDKSchedulesClient(TestSDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.team_ids = []
        self.schedules_ids = []
        self.account_member_ids = []
        self.uuid = self.generate_uuid()
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id="999a17ed-c7c3-4860-9024-d11c18fa5fa4"
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
                        "user": "3544118d-fbf5-41e5-ae6c-5",
                        "position": 1,
                    }
                ],
            }
        ]

        self.overrides = [
            {
                "name": "",
                "user": "3544118d-fbf5-41e5-ae6c-5",
                "start_time": "2024-07-29T11:54:34.745000Z",
                "end_time": "2024-07-29T18:29:59.999000Z",
            }
        ]

    def test_create_schedule(self):
        create_schedule = self.schedules_client.create_schedule(
            name=self.schedules_name,
            timezone="Asia/Kolkata",
            layers=self.layers,
            overrides=self.overrides,
        )

        self.schedules_ids.append(create_schedule.unique_id)
        assert create_schedule.name == self.schedules_name
        time.sleep(2)

    def test_get_all_schedules(self):
        get_all_schedules = self.schedules_client.get_all_schedules()
        time.sleep(2)

    def test_get_schedule_by_id(self):
        self.get_schedule_by_id = self.schedules_client.get_schedule_by_id(
            schedule_id=self.schedules_ids[0]
        )

        assert self.get_schedule_by_id.name == self.schedules_name
        time.sleep(2)

    def test_update_schedule(self):
        update_schedule = self.schedules_client.update_schedule(
            schedule=self.get_schedule_by_id,
            name="Test Schedule Updated",
        )
        assert update_schedule.name == "Test Schedule Updated"

    def test_delete_schedule(self):
        delete_schedule = self.schedules_client.delete_schedule(
            schedule=self.get_schedule_by_id
        )


@pytest.mark.services
class TestSDKServicesClient(TestSDKTeamsClient):
    def __init__(self):
        super().__init__()
        self.team_ids = []
        self.sla_ids = []
        self.priority_ids = []
        self.escalation_policy_ids = []
        self.service_ids = []
        # Making the Teams Client
        self.teams_client = TeamsClient(client=self.client)
        self.team_ids.append(self.create_team(self))
        # Making the Service Client
        self.service_client = self.teams_client.get_service_client(self.team_ids[0])
        self.team_by_id = self.teams_client.find_team_by_id(
            team_id="999a17ed-c7c3-4860-9024-d11c18fa5fa4"
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
                    {"target_type": 2, "target_id": "3544118d-fbf5-41e5-ae6c-5"}
                ],
                "position": 1,
            }
        ]
        create_escalation_policy = self.escalation_policy_client.create_esp(
            self.ep_name, rules=self.rule_build
        )

        # Appending the unique_id to the escalation_policy_ids list
        self.escalation_policy_ids.append(str(create_escalation_policy.unique_id))
        print("ids", self.escalation_policy_ids)
        time.sleep(2)
        # Create the Priority
        create_priority = self.priority_client.create_priority(
            name=self.priority_name,
            description="Priority Description",
            color="red",
        )

        # Appending the unique_id to the priority_ids list
        self.priority_ids.append(create_priority.unique_id)
        time.sleep(2)

        # Create the SLA
        create_sla = self.sla_client.create_sla(name="Test SLA", escalations=[])

        # Appending the unique_id to the sla_ids list
        self.sla_ids.append(create_sla.unique_id)

        time.sleep(2)

        # Finally create the service
        create_service = self.service_client.create_service(
            name=f"Test Service - {self.datetime_timestamp}",
            escalation_policy=self.escalation_policy_ids[0],
            team_priority=str(self.priority_ids[0]),
            sla=str(self.sla_ids[0]),
        )


@pytest.mark.integrations
class TestSDKIntegrationClient(TestSDKServicesClient):
    def __init__(self):
        super().__init__()
        self.service_ids = []
        integration_client = self.service_client.get_integration_client(
            svc=self.service_ids[0]
        )


@pytest.mark.sla
class TestSDKSLAClient(SDKTestingClient):
    pass


@pytest.mark.tags
class TestSDKTagsClient(SDKTestingClient):
    pass


@pytest.mark.tasktemplates
class TestSDKTaskTemplatesClient(SDKTestingClient):
    pass


if __name__ == "__main__":
    # escalations_client = TestSDKEscalationPolicyClient()
    # escalations_client.test_create_escalation_policy()

    # teams_client = TestSDKTeamsClient()
    # teams_client.test_create_team()
    # teams_client.test_find_team_by_id()
    # teams_client.test_list_team_member()
    # teams_client.test_add_team_member()
    # teams_client.test_find_team_member()
    # teams_client.test_update_team_member()
    # teams_client.test_delete_team_member()
    # teams_client.test_fetch_team_permissions()
    # teams_client.update_team_permissions()
    # teams_client.test_update_teams()
    # teams_client.test_delete_teams()

    # router_client = TestSDKGERClients()
    # router_client.test_create_router()
    # router_client.test_list_routers()
    # router_client.test_get_router_by_id()
    # router_client.test_update_router()
    # router_client.test_delete_router()

    # account_members = TestSDKAccountMembersClient()
    # account_members.test_account_members_invite()
    # account_members.test_account_member_update()
    # account_members.test_get_account_member()
    # account_members.test_get_all_account_members()
    # account_members.test_delete_account_member()

    # account_role = TestSDKAccountRolesClient()
    # account_role.test_create_account_role()
    # account_role.test_get_account_role()
    # account_role.test_list_account_roles()
    # account_role.test_update_account_role()
    # account_role.test_delete_account_role()

    # event = TestSDKEventsClient()
    # event.test_get_router_client()
    # event.test_create_event()

    # incidents = TestSDKIncidentsClient()
    # incidents.test_create_incident()
    # incidents.test_get_all_incidents()
    # incidents.test_get_alerts_by_incident()
    # incidents.test_update_incident()

    # incidents.test_create_incident_note()
    # incidents.test_get_all_incident_notes()
    # # get this checked tomorrow
    # # incidents.test_get_incident_note_by_id()
    # incidents.test_update_incident_note()
    # incidents.test_delete_incident_note()
    # # get this checked tomorrow - all of these below
    # incidents.test_create_incident_tag()
    # incidents.test_get_all_tags()
    # incidents.test_get_tag_by_id()
    # incidents.test_delete_incident_tag()

    # escalations_client = TestSDKEscalationPolicyClient()
    # escalations_client.test_create_escalation_policy()
    # escalations_client.test_get_esp_by_id()
    # escalations_client.test_update_esp()
    # escalations_client.test_get_all_policies()
    # escalations_client.test_delete_esp()

    # Run this, and ask what is "Maintenance_Template"
    # add Maintenance_Template to the model
    # maintenance_client = TestSDKMaintenanceClient()
    # maintenance_client.test_create_maintenance()
    # maintenance_client.test_get_all_maintenance()
    # maintenance_client.test_get_maintenance_by_id()
    # maintenance_client.test_update_maintenance_by_id()
    # maintenance_client.test_delete_maintenance()

    # postmortem_client = TestSDKPostMortemClient()
    # postmortem_client.test_create_postmortem()
    # postmortem_client.test_get_postmortem_by_id()
    # postmortem_client.test_update_postmortem()
    # postmortem_client.test_delete_postmortem()

    # priority_client = TestSDKPrioritiesClient()
    # priority_client.test_create_priority()
    # priority_client.test_get_all_priorities()
    # priority_client.test_get_priority_by_id()
    # priority_client.test_update_priority()
    # priority_client.test_delete_priority()

    # roles_client = TestSDKRolesClient()
    # roles_client.test_create_role()
    # roles_client.test_get_incident_role_by_id()
    # roles_client.test_update_incident_role()
    # roles_client.test_delete_incident_role()

    # schedules_client = TestSDKSchedulesClient()
    # schedules_client.test_create_schedule()
    # schedules_client.test_get_all_schedules()
    # schedules_client.test_get_schedule_by_id()
    # schedules_client.test_update_schedule()
    # schedules_client.test_delete_schedule()

    services_client = TestSDKServicesClient()
    services_client.test_create_service()

    pass
