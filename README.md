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

```python
import zenduty

class SDKTestingClient:
    def __init__(self):
        self.cred = ZendutyCredential("<ZENDUTY-API-TOKEN>")
        self.client = ZendutyClient(
            credential=self.cred, use_https=True
        )  # defaults to default service endpoint zenduty.com

@pytest.mark.teams
class SDKTeamsClient(SDKTestingClient):
    def __init__(self):
        super().__init__()
        self.teams_client = TeamsClient(client=self.client)
        self.team_member_id = "773c69f5-78f2-42ca-b3d9-b" # Random member id. 
        self.invite_url = "https://zenduty.com/api/invite/accept/"
        self.test_team_name = f"Team - {self.datetime_timestamp}"

    def create_team(self):
        create_team = self.teams_client.create_team(self.test_team_name)
        return create_team
```

It is important to note that each function returns a urllib3.response.HTTPResponse object.


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

    def test_account_members_invite(self):
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


#### DELETE - Delete an Account member
#### Delete a particular member of the team.


````python
delete_account_member = self.account_member_client.delete_account_member(account_member_id="<unique_id Of a member>")
````




## Running tests

There is a sample skeleton code in bin/. Add your access token to it and modify the object and function name for testing purposes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
