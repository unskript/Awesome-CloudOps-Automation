from typing import List
from pydantic import BaseModel, Field
from beartype import beartype
import argparse
from google.oauth2 import service_account

class InputSchema(BaseModel):
    role: str = Field(
        title = "role",
        description = "GCP user role to be removed"
    )
    member: str = Field(
        title = "member",
        description = "user's id to be removed"
    )
def modify_policy_remove_member(output):
    if output is None:
        return

    print(output)

@beartype
def modify_policy_remove_member(policy, role: str, member: str):
    """Removes a  member from a role binding.

        :type role: string
        :param role: user role to be removed.

        :type member: string
        :param member: user's id to be removed.

        :rtype: confirmation of removal of role."""

    service = discovery.build('iam', 'v1', credentials=credentials)
    # The resource for which the policy is being requested.
    resource = 'projects/my-project/serviceAccounts/my-service-account'
    # TODO: Update placeholder value.
    request = service.projects().serviceAccounts().getIamPolicy(resource=resource)
    response = request.execute()
    binding = next(b for b in policy["bindings"] if b["role"] == role)
    if "members" in binding and member in binding["members"]:
        binding["members"].remove(member)
    print(binding)
    print(role)
    return policy

# Initiate a Task object
task = Task(Workflow())

(err,hdl, args) = task.validate(vars=vars()) 
if err is None:
    task.execute(modify_policy_remove_member,
                 lego_printer=modify_policy_remove_member,
                 hdl=hdl,
                 args=args)