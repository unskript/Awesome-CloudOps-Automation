import pprint
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    role: str = Field(
        title = "Role",
        description = "GCP user role to be removed"
    )
    member: str = Field(
        title = "Member",
        description = "user's id to be removed"
    )
    resource: str = Field(
        title = "Resource",
        description = ('GCP Resource in the form of project/<PROJECT_ID>'
                       '/serviceAccounts/<SERVICE_ACCOUNT_NAME>')

    )
def gcp_remove_user_role_printer(output):
    if output is None:
        return
    pprint.pprint("User role removed successfully.")
    pprint.pprint(output)

def gcp_remove_user_role(policy, role: str, member: str, resource: str):
    """Removes a  member from a role binding.

        :type role: string
        :param role: user role to be removed.

        :type member: string
        :param member: user's id to be removed.
        
        :type resource: string
        :param resource: resource for which the policy is being requested.

        :rtype: confirmation of removal of role."""

    # TODO: Update placeholder value.
    binding = next(b for b in policy["bindings"] if b["role"] == role)
    if "members" in binding and member in binding["members"]:
        binding["members"].remove(member)
    return policy
