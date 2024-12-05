# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from . import _utilities

__all__ = [
    'GetCurrentUserResult',
    'AwaitableGetCurrentUserResult',
    'get_current_user',
    'get_current_user_output',
]

@pulumi.output_type
class GetCurrentUserResult:
    """
    A collection of values returned by getCurrentUser.
    """
    def __init__(__self__, acl_principal_id=None, alphanumeric=None, external_id=None, home=None, id=None, repos=None, user_name=None, workspace_url=None):
        if acl_principal_id and not isinstance(acl_principal_id, str):
            raise TypeError("Expected argument 'acl_principal_id' to be a str")
        pulumi.set(__self__, "acl_principal_id", acl_principal_id)
        if alphanumeric and not isinstance(alphanumeric, str):
            raise TypeError("Expected argument 'alphanumeric' to be a str")
        pulumi.set(__self__, "alphanumeric", alphanumeric)
        if external_id and not isinstance(external_id, str):
            raise TypeError("Expected argument 'external_id' to be a str")
        pulumi.set(__self__, "external_id", external_id)
        if home and not isinstance(home, str):
            raise TypeError("Expected argument 'home' to be a str")
        pulumi.set(__self__, "home", home)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if repos and not isinstance(repos, str):
            raise TypeError("Expected argument 'repos' to be a str")
        pulumi.set(__self__, "repos", repos)
        if user_name and not isinstance(user_name, str):
            raise TypeError("Expected argument 'user_name' to be a str")
        pulumi.set(__self__, "user_name", user_name)
        if workspace_url and not isinstance(workspace_url, str):
            raise TypeError("Expected argument 'workspace_url' to be a str")
        pulumi.set(__self__, "workspace_url", workspace_url)

    @property
    @pulumi.getter(name="aclPrincipalId")
    def acl_principal_id(self) -> str:
        return pulumi.get(self, "acl_principal_id")

    @property
    @pulumi.getter
    def alphanumeric(self) -> str:
        return pulumi.get(self, "alphanumeric")

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> str:
        return pulumi.get(self, "external_id")

    @property
    @pulumi.getter
    def home(self) -> str:
        return pulumi.get(self, "home")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def repos(self) -> str:
        return pulumi.get(self, "repos")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> str:
        return pulumi.get(self, "user_name")

    @property
    @pulumi.getter(name="workspaceUrl")
    def workspace_url(self) -> str:
        return pulumi.get(self, "workspace_url")


class AwaitableGetCurrentUserResult(GetCurrentUserResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCurrentUserResult(
            acl_principal_id=self.acl_principal_id,
            alphanumeric=self.alphanumeric,
            external_id=self.external_id,
            home=self.home,
            id=self.id,
            repos=self.repos,
            user_name=self.user_name,
            workspace_url=self.workspace_url)


def get_current_user(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCurrentUserResult:
    """
    > **Note** If you have a fully automated setup with workspaces created by MwsWorkspaces or azurerm_databricks_workspace, please make sure to add depends_on attribute in order to prevent _default auth: cannot configure default credentials_ errors.

    Retrieves information about User or databricks_service_principal, that is calling Databricks REST API. Might be useful in applying the same Pulumi by different users in the shared workspace for testing purposes.
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('databricks:index/getCurrentUser:getCurrentUser', __args__, opts=opts, typ=GetCurrentUserResult).value

    return AwaitableGetCurrentUserResult(
        acl_principal_id=pulumi.get(__ret__, 'acl_principal_id'),
        alphanumeric=pulumi.get(__ret__, 'alphanumeric'),
        external_id=pulumi.get(__ret__, 'external_id'),
        home=pulumi.get(__ret__, 'home'),
        id=pulumi.get(__ret__, 'id'),
        repos=pulumi.get(__ret__, 'repos'),
        user_name=pulumi.get(__ret__, 'user_name'),
        workspace_url=pulumi.get(__ret__, 'workspace_url'))
def get_current_user_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCurrentUserResult]:
    """
    > **Note** If you have a fully automated setup with workspaces created by MwsWorkspaces or azurerm_databricks_workspace, please make sure to add depends_on attribute in order to prevent _default auth: cannot configure default credentials_ errors.

    Retrieves information about User or databricks_service_principal, that is calling Databricks REST API. Might be useful in applying the same Pulumi by different users in the shared workspace for testing purposes.
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('databricks:index/getCurrentUser:getCurrentUser', __args__, opts=opts, typ=GetCurrentUserResult)
    return __ret__.apply(lambda __response__: GetCurrentUserResult(
        acl_principal_id=pulumi.get(__response__, 'acl_principal_id'),
        alphanumeric=pulumi.get(__response__, 'alphanumeric'),
        external_id=pulumi.get(__response__, 'external_id'),
        home=pulumi.get(__response__, 'home'),
        id=pulumi.get(__response__, 'id'),
        repos=pulumi.get(__response__, 'repos'),
        user_name=pulumi.get(__response__, 'user_name'),
        workspace_url=pulumi.get(__response__, 'workspace_url')))
