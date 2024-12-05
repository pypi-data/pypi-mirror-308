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

__all__ = ['GroupArgs', 'Group']

@pulumi.input_type
class GroupArgs:
    def __init__(__self__, *,
                 acl_principal_id: Optional[pulumi.Input[str]] = None,
                 allow_cluster_create: Optional[pulumi.Input[bool]] = None,
                 allow_instance_pool_create: Optional[pulumi.Input[bool]] = None,
                 databricks_sql_access: Optional[pulumi.Input[bool]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 external_id: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 workspace_access: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Group resource.
        :param pulumi.Input[str] acl_principal_id: identifier for use in databricks_access_control_rule_set, e.g. `groups/Some Group`.
        :param pulumi.Input[bool] allow_cluster_create: This is a field to allow the group to have cluster create privileges. More fine grained permissions could be assigned with Permissions and cluster_id argument. Everyone without `allow_cluster_create` argument set, but with permission to use Cluster Policy would be able to create clusters, but within boundaries of that specific policy.
        :param pulumi.Input[bool] allow_instance_pool_create: This is a field to allow the group to have instance pool create privileges. More fine grained permissions could be assigned with Permissions and instance_pool_id argument.
        :param pulumi.Input[bool] databricks_sql_access: This is a field to allow the group to have access to [Databricks SQL](https://databricks.com/product/databricks-sql) feature in User Interface and through databricks_sql_endpoint.
        :param pulumi.Input[str] display_name: This is the display name for the given group.
        :param pulumi.Input[str] external_id: ID of the group in an external identity provider.
        :param pulumi.Input[bool] force: Ignore `cannot create group: Group with name X already exists.` errors and implicitly import the specific group into Pulumi state, enforcing entitlements defined in the instance of resource. _This functionality is experimental_ and is designed to simplify corner cases, like Azure Active Directory synchronisation.
        :param pulumi.Input[bool] workspace_access: This is a field to allow the group to have access to Databricks Workspace.
        """
        if acl_principal_id is not None:
            pulumi.set(__self__, "acl_principal_id", acl_principal_id)
        if allow_cluster_create is not None:
            pulumi.set(__self__, "allow_cluster_create", allow_cluster_create)
        if allow_instance_pool_create is not None:
            pulumi.set(__self__, "allow_instance_pool_create", allow_instance_pool_create)
        if databricks_sql_access is not None:
            pulumi.set(__self__, "databricks_sql_access", databricks_sql_access)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if external_id is not None:
            pulumi.set(__self__, "external_id", external_id)
        if force is not None:
            pulumi.set(__self__, "force", force)
        if url is not None:
            pulumi.set(__self__, "url", url)
        if workspace_access is not None:
            pulumi.set(__self__, "workspace_access", workspace_access)

    @property
    @pulumi.getter(name="aclPrincipalId")
    def acl_principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        identifier for use in databricks_access_control_rule_set, e.g. `groups/Some Group`.
        """
        return pulumi.get(self, "acl_principal_id")

    @acl_principal_id.setter
    def acl_principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "acl_principal_id", value)

    @property
    @pulumi.getter(name="allowClusterCreate")
    def allow_cluster_create(self) -> Optional[pulumi.Input[bool]]:
        """
        This is a field to allow the group to have cluster create privileges. More fine grained permissions could be assigned with Permissions and cluster_id argument. Everyone without `allow_cluster_create` argument set, but with permission to use Cluster Policy would be able to create clusters, but within boundaries of that specific policy.
        """
        return pulumi.get(self, "allow_cluster_create")

    @allow_cluster_create.setter
    def allow_cluster_create(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_cluster_create", value)

    @property
    @pulumi.getter(name="allowInstancePoolCreate")
    def allow_instance_pool_create(self) -> Optional[pulumi.Input[bool]]:
        """
        This is a field to allow the group to have instance pool create privileges. More fine grained permissions could be assigned with Permissions and instance_pool_id argument.
        """
        return pulumi.get(self, "allow_instance_pool_create")

    @allow_instance_pool_create.setter
    def allow_instance_pool_create(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_instance_pool_create", value)

    @property
    @pulumi.getter(name="databricksSqlAccess")
    def databricks_sql_access(self) -> Optional[pulumi.Input[bool]]:
        """
        This is a field to allow the group to have access to [Databricks SQL](https://databricks.com/product/databricks-sql) feature in User Interface and through databricks_sql_endpoint.
        """
        return pulumi.get(self, "databricks_sql_access")

    @databricks_sql_access.setter
    def databricks_sql_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "databricks_sql_access", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        This is the display name for the given group.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the group in an external identity provider.
        """
        return pulumi.get(self, "external_id")

    @external_id.setter
    def external_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "external_id", value)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        Ignore `cannot create group: Group with name X already exists.` errors and implicitly import the specific group into Pulumi state, enforcing entitlements defined in the instance of resource. _This functionality is experimental_ and is designed to simplify corner cases, like Azure Active Directory synchronisation.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter(name="workspaceAccess")
    def workspace_access(self) -> Optional[pulumi.Input[bool]]:
        """
        This is a field to allow the group to have access to Databricks Workspace.
        """
        return pulumi.get(self, "workspace_access")

    @workspace_access.setter
    def workspace_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "workspace_access", value)


@pulumi.input_type
class _GroupState:
    def __init__(__self__, *,
                 acl_principal_id: Optional[pulumi.Input[str]] = None,
                 allow_cluster_create: Optional[pulumi.Input[bool]] = None,
                 allow_instance_pool_create: Optional[pulumi.Input[bool]] = None,
                 databricks_sql_access: Optional[pulumi.Input[bool]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 external_id: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 workspace_access: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering Group resources.
        :param pulumi.Input[str] acl_principal_id: identifier for use in databricks_access_control_rule_set, e.g. `groups/Some Group`.
        :param pulumi.Input[bool] allow_cluster_create: This is a field to allow the group to have cluster create privileges. More fine grained permissions could be assigned with Permissions and cluster_id argument. Everyone without `allow_cluster_create` argument set, but with permission to use Cluster Policy would be able to create clusters, but within boundaries of that specific policy.
        :param pulumi.Input[bool] allow_instance_pool_create: This is a field to allow the group to have instance pool create privileges. More fine grained permissions could be assigned with Permissions and instance_pool_id argument.
        :param pulumi.Input[bool] databricks_sql_access: This is a field to allow the group to have access to [Databricks SQL](https://databricks.com/product/databricks-sql) feature in User Interface and through databricks_sql_endpoint.
        :param pulumi.Input[str] display_name: This is the display name for the given group.
        :param pulumi.Input[str] external_id: ID of the group in an external identity provider.
        :param pulumi.Input[bool] force: Ignore `cannot create group: Group with name X already exists.` errors and implicitly import the specific group into Pulumi state, enforcing entitlements defined in the instance of resource. _This functionality is experimental_ and is designed to simplify corner cases, like Azure Active Directory synchronisation.
        :param pulumi.Input[bool] workspace_access: This is a field to allow the group to have access to Databricks Workspace.
        """
        if acl_principal_id is not None:
            pulumi.set(__self__, "acl_principal_id", acl_principal_id)
        if allow_cluster_create is not None:
            pulumi.set(__self__, "allow_cluster_create", allow_cluster_create)
        if allow_instance_pool_create is not None:
            pulumi.set(__self__, "allow_instance_pool_create", allow_instance_pool_create)
        if databricks_sql_access is not None:
            pulumi.set(__self__, "databricks_sql_access", databricks_sql_access)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if external_id is not None:
            pulumi.set(__self__, "external_id", external_id)
        if force is not None:
            pulumi.set(__self__, "force", force)
        if url is not None:
            pulumi.set(__self__, "url", url)
        if workspace_access is not None:
            pulumi.set(__self__, "workspace_access", workspace_access)

    @property
    @pulumi.getter(name="aclPrincipalId")
    def acl_principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        identifier for use in databricks_access_control_rule_set, e.g. `groups/Some Group`.
        """
        return pulumi.get(self, "acl_principal_id")

    @acl_principal_id.setter
    def acl_principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "acl_principal_id", value)

    @property
    @pulumi.getter(name="allowClusterCreate")
    def allow_cluster_create(self) -> Optional[pulumi.Input[bool]]:
        """
        This is a field to allow the group to have cluster create privileges. More fine grained permissions could be assigned with Permissions and cluster_id argument. Everyone without `allow_cluster_create` argument set, but with permission to use Cluster Policy would be able to create clusters, but within boundaries of that specific policy.
        """
        return pulumi.get(self, "allow_cluster_create")

    @allow_cluster_create.setter
    def allow_cluster_create(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_cluster_create", value)

    @property
    @pulumi.getter(name="allowInstancePoolCreate")
    def allow_instance_pool_create(self) -> Optional[pulumi.Input[bool]]:
        """
        This is a field to allow the group to have instance pool create privileges. More fine grained permissions could be assigned with Permissions and instance_pool_id argument.
        """
        return pulumi.get(self, "allow_instance_pool_create")

    @allow_instance_pool_create.setter
    def allow_instance_pool_create(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_instance_pool_create", value)

    @property
    @pulumi.getter(name="databricksSqlAccess")
    def databricks_sql_access(self) -> Optional[pulumi.Input[bool]]:
        """
        This is a field to allow the group to have access to [Databricks SQL](https://databricks.com/product/databricks-sql) feature in User Interface and through databricks_sql_endpoint.
        """
        return pulumi.get(self, "databricks_sql_access")

    @databricks_sql_access.setter
    def databricks_sql_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "databricks_sql_access", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        This is the display name for the given group.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the group in an external identity provider.
        """
        return pulumi.get(self, "external_id")

    @external_id.setter
    def external_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "external_id", value)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        Ignore `cannot create group: Group with name X already exists.` errors and implicitly import the specific group into Pulumi state, enforcing entitlements defined in the instance of resource. _This functionality is experimental_ and is designed to simplify corner cases, like Azure Active Directory synchronisation.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter(name="workspaceAccess")
    def workspace_access(self) -> Optional[pulumi.Input[bool]]:
        """
        This is a field to allow the group to have access to Databricks Workspace.
        """
        return pulumi.get(self, "workspace_access")

    @workspace_access.setter
    def workspace_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "workspace_access", value)


class Group(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acl_principal_id: Optional[pulumi.Input[str]] = None,
                 allow_cluster_create: Optional[pulumi.Input[bool]] = None,
                 allow_instance_pool_create: Optional[pulumi.Input[bool]] = None,
                 databricks_sql_access: Optional[pulumi.Input[bool]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 external_id: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 workspace_access: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        This resource allows you to manage both [account groups and workspace-local groups](https://docs.databricks.com/administration-guide/users-groups/groups.html). You can use the GroupMember resource to assign Databricks users, service principals as well as other groups as members of the group. This is useful if you are using an application to sync users & groups with SCIM API.

        > To assign an account level group to a workspace use databricks_mws_permission_assignment.

        > Entitlements, like, `allow_cluster_create`, `allow_instance_pool_create`, `databricks_sql_access`, `workspace_access` applicable only for workspace-level groups.  Use Entitlements resource to assign entitlements inside a workspace to account-level groups.

        To create account groups in the Databricks account, the provider must be configured accordingly. On AWS deployment with `host = "https://accounts.cloud.databricks.com"` and `account_id = "00000000-0000-0000-0000-000000000000"`. On Azure deployments `host = "https://accounts.azuredatabricks.net"`, `account_id = "00000000-0000-0000-0000-000000000000"` and using AAD tokens as authentication.

        Recommended to use along with Identity Provider SCIM provisioning to populate users into those groups:

        * [Azure Active Directory](https://docs.microsoft.com/en-us/azure/databricks/administration-guide/users-groups/scim/aad)
        * [Okta](https://docs.databricks.com/administration-guide/users-groups/scim/okta.html)
        * [OneLogin](https://docs.databricks.com/administration-guide/users-groups/scim/onelogin.html)

        ## Example Usage

        Creating some group

        ```python
        import pulumi
        import pulumi_databricks as databricks

        this = databricks.Group("this",
            display_name="Some Group",
            allow_cluster_create=True,
            allow_instance_pool_create=True)
        ```

        Adding User as GroupMember of some group

        ```python
        import pulumi
        import pulumi_databricks as databricks

        this = databricks.Group("this",
            display_name="Some Group",
            allow_cluster_create=True,
            allow_instance_pool_create=True)
        this_user = databricks.User("this", user_name="someone@example.com")
        vip_member = databricks.GroupMember("vip_member",
            group_id=this.id,
            member_id=this_user.id)
        ```

        Creating group in AWS Databricks account:

        ```python
        import pulumi
        import pulumi_databricks as databricks

        this = databricks.Group("this", display_name="Some Group")
        ```

        Creating group in Azure Databricks account:

        ```python
        import pulumi
        import pulumi_databricks as databricks

        this = databricks.Group("this", display_name="Some Group")
        ```

        ## Import

        You can import a `databricks_group` resource with the name `my_group` like the following:

        bash

        ```sh
        $ pulumi import databricks:index/group:Group my_group <group_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] acl_principal_id: identifier for use in databricks_access_control_rule_set, e.g. `groups/Some Group`.
        :param pulumi.Input[bool] allow_cluster_create: This is a field to allow the group to have cluster create privileges. More fine grained permissions could be assigned with Permissions and cluster_id argument. Everyone without `allow_cluster_create` argument set, but with permission to use Cluster Policy would be able to create clusters, but within boundaries of that specific policy.
        :param pulumi.Input[bool] allow_instance_pool_create: This is a field to allow the group to have instance pool create privileges. More fine grained permissions could be assigned with Permissions and instance_pool_id argument.
        :param pulumi.Input[bool] databricks_sql_access: This is a field to allow the group to have access to [Databricks SQL](https://databricks.com/product/databricks-sql) feature in User Interface and through databricks_sql_endpoint.
        :param pulumi.Input[str] display_name: This is the display name for the given group.
        :param pulumi.Input[str] external_id: ID of the group in an external identity provider.
        :param pulumi.Input[bool] force: Ignore `cannot create group: Group with name X already exists.` errors and implicitly import the specific group into Pulumi state, enforcing entitlements defined in the instance of resource. _This functionality is experimental_ and is designed to simplify corner cases, like Azure Active Directory synchronisation.
        :param pulumi.Input[bool] workspace_access: This is a field to allow the group to have access to Databricks Workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[GroupArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource allows you to manage both [account groups and workspace-local groups](https://docs.databricks.com/administration-guide/users-groups/groups.html). You can use the GroupMember resource to assign Databricks users, service principals as well as other groups as members of the group. This is useful if you are using an application to sync users & groups with SCIM API.

        > To assign an account level group to a workspace use databricks_mws_permission_assignment.

        > Entitlements, like, `allow_cluster_create`, `allow_instance_pool_create`, `databricks_sql_access`, `workspace_access` applicable only for workspace-level groups.  Use Entitlements resource to assign entitlements inside a workspace to account-level groups.

        To create account groups in the Databricks account, the provider must be configured accordingly. On AWS deployment with `host = "https://accounts.cloud.databricks.com"` and `account_id = "00000000-0000-0000-0000-000000000000"`. On Azure deployments `host = "https://accounts.azuredatabricks.net"`, `account_id = "00000000-0000-0000-0000-000000000000"` and using AAD tokens as authentication.

        Recommended to use along with Identity Provider SCIM provisioning to populate users into those groups:

        * [Azure Active Directory](https://docs.microsoft.com/en-us/azure/databricks/administration-guide/users-groups/scim/aad)
        * [Okta](https://docs.databricks.com/administration-guide/users-groups/scim/okta.html)
        * [OneLogin](https://docs.databricks.com/administration-guide/users-groups/scim/onelogin.html)

        ## Example Usage

        Creating some group

        ```python
        import pulumi
        import pulumi_databricks as databricks

        this = databricks.Group("this",
            display_name="Some Group",
            allow_cluster_create=True,
            allow_instance_pool_create=True)
        ```

        Adding User as GroupMember of some group

        ```python
        import pulumi
        import pulumi_databricks as databricks

        this = databricks.Group("this",
            display_name="Some Group",
            allow_cluster_create=True,
            allow_instance_pool_create=True)
        this_user = databricks.User("this", user_name="someone@example.com")
        vip_member = databricks.GroupMember("vip_member",
            group_id=this.id,
            member_id=this_user.id)
        ```

        Creating group in AWS Databricks account:

        ```python
        import pulumi
        import pulumi_databricks as databricks

        this = databricks.Group("this", display_name="Some Group")
        ```

        Creating group in Azure Databricks account:

        ```python
        import pulumi
        import pulumi_databricks as databricks

        this = databricks.Group("this", display_name="Some Group")
        ```

        ## Import

        You can import a `databricks_group` resource with the name `my_group` like the following:

        bash

        ```sh
        $ pulumi import databricks:index/group:Group my_group <group_id>
        ```

        :param str resource_name: The name of the resource.
        :param GroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acl_principal_id: Optional[pulumi.Input[str]] = None,
                 allow_cluster_create: Optional[pulumi.Input[bool]] = None,
                 allow_instance_pool_create: Optional[pulumi.Input[bool]] = None,
                 databricks_sql_access: Optional[pulumi.Input[bool]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 external_id: Optional[pulumi.Input[str]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 workspace_access: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GroupArgs.__new__(GroupArgs)

            __props__.__dict__["acl_principal_id"] = acl_principal_id
            __props__.__dict__["allow_cluster_create"] = allow_cluster_create
            __props__.__dict__["allow_instance_pool_create"] = allow_instance_pool_create
            __props__.__dict__["databricks_sql_access"] = databricks_sql_access
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["external_id"] = external_id
            __props__.__dict__["force"] = force
            __props__.__dict__["url"] = url
            __props__.__dict__["workspace_access"] = workspace_access
        super(Group, __self__).__init__(
            'databricks:index/group:Group',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            acl_principal_id: Optional[pulumi.Input[str]] = None,
            allow_cluster_create: Optional[pulumi.Input[bool]] = None,
            allow_instance_pool_create: Optional[pulumi.Input[bool]] = None,
            databricks_sql_access: Optional[pulumi.Input[bool]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            external_id: Optional[pulumi.Input[str]] = None,
            force: Optional[pulumi.Input[bool]] = None,
            url: Optional[pulumi.Input[str]] = None,
            workspace_access: Optional[pulumi.Input[bool]] = None) -> 'Group':
        """
        Get an existing Group resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] acl_principal_id: identifier for use in databricks_access_control_rule_set, e.g. `groups/Some Group`.
        :param pulumi.Input[bool] allow_cluster_create: This is a field to allow the group to have cluster create privileges. More fine grained permissions could be assigned with Permissions and cluster_id argument. Everyone without `allow_cluster_create` argument set, but with permission to use Cluster Policy would be able to create clusters, but within boundaries of that specific policy.
        :param pulumi.Input[bool] allow_instance_pool_create: This is a field to allow the group to have instance pool create privileges. More fine grained permissions could be assigned with Permissions and instance_pool_id argument.
        :param pulumi.Input[bool] databricks_sql_access: This is a field to allow the group to have access to [Databricks SQL](https://databricks.com/product/databricks-sql) feature in User Interface and through databricks_sql_endpoint.
        :param pulumi.Input[str] display_name: This is the display name for the given group.
        :param pulumi.Input[str] external_id: ID of the group in an external identity provider.
        :param pulumi.Input[bool] force: Ignore `cannot create group: Group with name X already exists.` errors and implicitly import the specific group into Pulumi state, enforcing entitlements defined in the instance of resource. _This functionality is experimental_ and is designed to simplify corner cases, like Azure Active Directory synchronisation.
        :param pulumi.Input[bool] workspace_access: This is a field to allow the group to have access to Databricks Workspace.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GroupState.__new__(_GroupState)

        __props__.__dict__["acl_principal_id"] = acl_principal_id
        __props__.__dict__["allow_cluster_create"] = allow_cluster_create
        __props__.__dict__["allow_instance_pool_create"] = allow_instance_pool_create
        __props__.__dict__["databricks_sql_access"] = databricks_sql_access
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["external_id"] = external_id
        __props__.__dict__["force"] = force
        __props__.__dict__["url"] = url
        __props__.__dict__["workspace_access"] = workspace_access
        return Group(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="aclPrincipalId")
    def acl_principal_id(self) -> pulumi.Output[str]:
        """
        identifier for use in databricks_access_control_rule_set, e.g. `groups/Some Group`.
        """
        return pulumi.get(self, "acl_principal_id")

    @property
    @pulumi.getter(name="allowClusterCreate")
    def allow_cluster_create(self) -> pulumi.Output[Optional[bool]]:
        """
        This is a field to allow the group to have cluster create privileges. More fine grained permissions could be assigned with Permissions and cluster_id argument. Everyone without `allow_cluster_create` argument set, but with permission to use Cluster Policy would be able to create clusters, but within boundaries of that specific policy.
        """
        return pulumi.get(self, "allow_cluster_create")

    @property
    @pulumi.getter(name="allowInstancePoolCreate")
    def allow_instance_pool_create(self) -> pulumi.Output[Optional[bool]]:
        """
        This is a field to allow the group to have instance pool create privileges. More fine grained permissions could be assigned with Permissions and instance_pool_id argument.
        """
        return pulumi.get(self, "allow_instance_pool_create")

    @property
    @pulumi.getter(name="databricksSqlAccess")
    def databricks_sql_access(self) -> pulumi.Output[Optional[bool]]:
        """
        This is a field to allow the group to have access to [Databricks SQL](https://databricks.com/product/databricks-sql) feature in User Interface and through databricks_sql_endpoint.
        """
        return pulumi.get(self, "databricks_sql_access")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        This is the display name for the given group.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="externalId")
    def external_id(self) -> pulumi.Output[Optional[str]]:
        """
        ID of the group in an external identity provider.
        """
        return pulumi.get(self, "external_id")

    @property
    @pulumi.getter
    def force(self) -> pulumi.Output[Optional[bool]]:
        """
        Ignore `cannot create group: Group with name X already exists.` errors and implicitly import the specific group into Pulumi state, enforcing entitlements defined in the instance of resource. _This functionality is experimental_ and is designed to simplify corner cases, like Azure Active Directory synchronisation.
        """
        return pulumi.get(self, "force")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        return pulumi.get(self, "url")

    @property
    @pulumi.getter(name="workspaceAccess")
    def workspace_access(self) -> pulumi.Output[Optional[bool]]:
        """
        This is a field to allow the group to have access to Databricks Workspace.
        """
        return pulumi.get(self, "workspace_access")

