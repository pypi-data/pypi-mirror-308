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

__all__ = ['WorkspaceBindingArgs', 'WorkspaceBinding']

@pulumi.input_type
class WorkspaceBindingArgs:
    def __init__(__self__, *,
                 binding_type: Optional[pulumi.Input[str]] = None,
                 catalog_name: Optional[pulumi.Input[str]] = None,
                 securable_name: Optional[pulumi.Input[str]] = None,
                 securable_type: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a WorkspaceBinding resource.
        :param pulumi.Input[str] binding_type: Binding mode. Default to `BINDING_TYPE_READ_WRITE`. Possible values are `BINDING_TYPE_READ_ONLY`, `BINDING_TYPE_READ_WRITE`.
        :param pulumi.Input[str] securable_name: Name of securable. Change forces creation of a new resource.
        :param pulumi.Input[str] securable_type: Type of securable. Can be `catalog`, `external-location` or `storage-credential`. Default to `catalog`. Change forces creation of a new resource.
        :param pulumi.Input[str] workspace_id: ID of the workspace. Change forces creation of a new resource.
        """
        if binding_type is not None:
            pulumi.set(__self__, "binding_type", binding_type)
        if catalog_name is not None:
            warnings.warn("""Please use 'securable_name' and 'securable_type instead.""", DeprecationWarning)
            pulumi.log.warn("""catalog_name is deprecated: Please use 'securable_name' and 'securable_type instead.""")
        if catalog_name is not None:
            pulumi.set(__self__, "catalog_name", catalog_name)
        if securable_name is not None:
            pulumi.set(__self__, "securable_name", securable_name)
        if securable_type is not None:
            pulumi.set(__self__, "securable_type", securable_type)
        if workspace_id is not None:
            pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="bindingType")
    def binding_type(self) -> Optional[pulumi.Input[str]]:
        """
        Binding mode. Default to `BINDING_TYPE_READ_WRITE`. Possible values are `BINDING_TYPE_READ_ONLY`, `BINDING_TYPE_READ_WRITE`.
        """
        return pulumi.get(self, "binding_type")

    @binding_type.setter
    def binding_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "binding_type", value)

    @property
    @pulumi.getter(name="catalogName")
    @_utilities.deprecated("""Please use 'securable_name' and 'securable_type instead.""")
    def catalog_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "catalog_name")

    @catalog_name.setter
    def catalog_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "catalog_name", value)

    @property
    @pulumi.getter(name="securableName")
    def securable_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of securable. Change forces creation of a new resource.
        """
        return pulumi.get(self, "securable_name")

    @securable_name.setter
    def securable_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "securable_name", value)

    @property
    @pulumi.getter(name="securableType")
    def securable_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of securable. Can be `catalog`, `external-location` or `storage-credential`. Default to `catalog`. Change forces creation of a new resource.
        """
        return pulumi.get(self, "securable_type")

    @securable_type.setter
    def securable_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "securable_type", value)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the workspace. Change forces creation of a new resource.
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workspace_id", value)


@pulumi.input_type
class _WorkspaceBindingState:
    def __init__(__self__, *,
                 binding_type: Optional[pulumi.Input[str]] = None,
                 catalog_name: Optional[pulumi.Input[str]] = None,
                 securable_name: Optional[pulumi.Input[str]] = None,
                 securable_type: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering WorkspaceBinding resources.
        :param pulumi.Input[str] binding_type: Binding mode. Default to `BINDING_TYPE_READ_WRITE`. Possible values are `BINDING_TYPE_READ_ONLY`, `BINDING_TYPE_READ_WRITE`.
        :param pulumi.Input[str] securable_name: Name of securable. Change forces creation of a new resource.
        :param pulumi.Input[str] securable_type: Type of securable. Can be `catalog`, `external-location` or `storage-credential`. Default to `catalog`. Change forces creation of a new resource.
        :param pulumi.Input[str] workspace_id: ID of the workspace. Change forces creation of a new resource.
        """
        if binding_type is not None:
            pulumi.set(__self__, "binding_type", binding_type)
        if catalog_name is not None:
            warnings.warn("""Please use 'securable_name' and 'securable_type instead.""", DeprecationWarning)
            pulumi.log.warn("""catalog_name is deprecated: Please use 'securable_name' and 'securable_type instead.""")
        if catalog_name is not None:
            pulumi.set(__self__, "catalog_name", catalog_name)
        if securable_name is not None:
            pulumi.set(__self__, "securable_name", securable_name)
        if securable_type is not None:
            pulumi.set(__self__, "securable_type", securable_type)
        if workspace_id is not None:
            pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="bindingType")
    def binding_type(self) -> Optional[pulumi.Input[str]]:
        """
        Binding mode. Default to `BINDING_TYPE_READ_WRITE`. Possible values are `BINDING_TYPE_READ_ONLY`, `BINDING_TYPE_READ_WRITE`.
        """
        return pulumi.get(self, "binding_type")

    @binding_type.setter
    def binding_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "binding_type", value)

    @property
    @pulumi.getter(name="catalogName")
    @_utilities.deprecated("""Please use 'securable_name' and 'securable_type instead.""")
    def catalog_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "catalog_name")

    @catalog_name.setter
    def catalog_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "catalog_name", value)

    @property
    @pulumi.getter(name="securableName")
    def securable_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of securable. Change forces creation of a new resource.
        """
        return pulumi.get(self, "securable_name")

    @securable_name.setter
    def securable_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "securable_name", value)

    @property
    @pulumi.getter(name="securableType")
    def securable_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of securable. Can be `catalog`, `external-location` or `storage-credential`. Default to `catalog`. Change forces creation of a new resource.
        """
        return pulumi.get(self, "securable_type")

    @securable_type.setter
    def securable_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "securable_type", value)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the workspace. Change forces creation of a new resource.
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workspace_id", value)


class WorkspaceBinding(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 binding_type: Optional[pulumi.Input[str]] = None,
                 catalog_name: Optional[pulumi.Input[str]] = None,
                 securable_name: Optional[pulumi.Input[str]] = None,
                 securable_type: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        > This resource can only be used with a workspace-level provider!

        If you use workspaces to isolate user data access, you may want to limit access to catalog, external locations or storage credentials from specific workspaces in your account, also known as workspace binding

        By default, Databricks assigns the securable to all workspaces attached to the current metastore. By using `WorkspaceBinding`, the securable will be unassigned from all workspaces and only assigned explicitly using this resource.

        > To use this resource the securable must have its isolation mode set to `ISOLATED` (for databricks_catalog) or `ISOLATION_MODE_ISOLATED` (for  (for ExternalLocation or databricks_storage_credential) for the `isolation_mode` attribute. Alternatively, the isolation mode can be set using the UI or API by following [this guide](https://docs.databricks.com/data-governance/unity-catalog/create-catalogs.html#configuration), [this guide](https://docs.databricks.com/en/connect/unity-catalog/external-locations.html#workspace-binding) or [this guide](https://docs.databricks.com/en/connect/unity-catalog/storage-credentials.html#optional-assign-a-storage-credential-to-specific-workspaces).

        > If the securable's isolation mode was set to `ISOLATED` using Pulumi then the securable will have been automatically bound to the workspace it was created from.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_databricks as databricks

        sandbox = databricks.Catalog("sandbox",
            name="sandbox",
            isolation_mode="ISOLATED")
        sandbox_workspace_binding = databricks.WorkspaceBinding("sandbox",
            securable_name=sandbox.name,
            workspace_id=other["workspaceId"])
        ```

        ## Import

        This resource can be imported by using combination of workspace ID, securable type and name:

        ```sh
        $ pulumi import databricks:index/workspaceBinding:WorkspaceBinding this "<workspace_id>|<securable_type>|<securable_name>"
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] binding_type: Binding mode. Default to `BINDING_TYPE_READ_WRITE`. Possible values are `BINDING_TYPE_READ_ONLY`, `BINDING_TYPE_READ_WRITE`.
        :param pulumi.Input[str] securable_name: Name of securable. Change forces creation of a new resource.
        :param pulumi.Input[str] securable_type: Type of securable. Can be `catalog`, `external-location` or `storage-credential`. Default to `catalog`. Change forces creation of a new resource.
        :param pulumi.Input[str] workspace_id: ID of the workspace. Change forces creation of a new resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[WorkspaceBindingArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        > This resource can only be used with a workspace-level provider!

        If you use workspaces to isolate user data access, you may want to limit access to catalog, external locations or storage credentials from specific workspaces in your account, also known as workspace binding

        By default, Databricks assigns the securable to all workspaces attached to the current metastore. By using `WorkspaceBinding`, the securable will be unassigned from all workspaces and only assigned explicitly using this resource.

        > To use this resource the securable must have its isolation mode set to `ISOLATED` (for databricks_catalog) or `ISOLATION_MODE_ISOLATED` (for  (for ExternalLocation or databricks_storage_credential) for the `isolation_mode` attribute. Alternatively, the isolation mode can be set using the UI or API by following [this guide](https://docs.databricks.com/data-governance/unity-catalog/create-catalogs.html#configuration), [this guide](https://docs.databricks.com/en/connect/unity-catalog/external-locations.html#workspace-binding) or [this guide](https://docs.databricks.com/en/connect/unity-catalog/storage-credentials.html#optional-assign-a-storage-credential-to-specific-workspaces).

        > If the securable's isolation mode was set to `ISOLATED` using Pulumi then the securable will have been automatically bound to the workspace it was created from.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_databricks as databricks

        sandbox = databricks.Catalog("sandbox",
            name="sandbox",
            isolation_mode="ISOLATED")
        sandbox_workspace_binding = databricks.WorkspaceBinding("sandbox",
            securable_name=sandbox.name,
            workspace_id=other["workspaceId"])
        ```

        ## Import

        This resource can be imported by using combination of workspace ID, securable type and name:

        ```sh
        $ pulumi import databricks:index/workspaceBinding:WorkspaceBinding this "<workspace_id>|<securable_type>|<securable_name>"
        ```

        :param str resource_name: The name of the resource.
        :param WorkspaceBindingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WorkspaceBindingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 binding_type: Optional[pulumi.Input[str]] = None,
                 catalog_name: Optional[pulumi.Input[str]] = None,
                 securable_name: Optional[pulumi.Input[str]] = None,
                 securable_type: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WorkspaceBindingArgs.__new__(WorkspaceBindingArgs)

            __props__.__dict__["binding_type"] = binding_type
            __props__.__dict__["catalog_name"] = catalog_name
            __props__.__dict__["securable_name"] = securable_name
            __props__.__dict__["securable_type"] = securable_type
            __props__.__dict__["workspace_id"] = workspace_id
        super(WorkspaceBinding, __self__).__init__(
            'databricks:index/workspaceBinding:WorkspaceBinding',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            binding_type: Optional[pulumi.Input[str]] = None,
            catalog_name: Optional[pulumi.Input[str]] = None,
            securable_name: Optional[pulumi.Input[str]] = None,
            securable_type: Optional[pulumi.Input[str]] = None,
            workspace_id: Optional[pulumi.Input[str]] = None) -> 'WorkspaceBinding':
        """
        Get an existing WorkspaceBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] binding_type: Binding mode. Default to `BINDING_TYPE_READ_WRITE`. Possible values are `BINDING_TYPE_READ_ONLY`, `BINDING_TYPE_READ_WRITE`.
        :param pulumi.Input[str] securable_name: Name of securable. Change forces creation of a new resource.
        :param pulumi.Input[str] securable_type: Type of securable. Can be `catalog`, `external-location` or `storage-credential`. Default to `catalog`. Change forces creation of a new resource.
        :param pulumi.Input[str] workspace_id: ID of the workspace. Change forces creation of a new resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _WorkspaceBindingState.__new__(_WorkspaceBindingState)

        __props__.__dict__["binding_type"] = binding_type
        __props__.__dict__["catalog_name"] = catalog_name
        __props__.__dict__["securable_name"] = securable_name
        __props__.__dict__["securable_type"] = securable_type
        __props__.__dict__["workspace_id"] = workspace_id
        return WorkspaceBinding(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="bindingType")
    def binding_type(self) -> pulumi.Output[Optional[str]]:
        """
        Binding mode. Default to `BINDING_TYPE_READ_WRITE`. Possible values are `BINDING_TYPE_READ_ONLY`, `BINDING_TYPE_READ_WRITE`.
        """
        return pulumi.get(self, "binding_type")

    @property
    @pulumi.getter(name="catalogName")
    @_utilities.deprecated("""Please use 'securable_name' and 'securable_type instead.""")
    def catalog_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "catalog_name")

    @property
    @pulumi.getter(name="securableName")
    def securable_name(self) -> pulumi.Output[str]:
        """
        Name of securable. Change forces creation of a new resource.
        """
        return pulumi.get(self, "securable_name")

    @property
    @pulumi.getter(name="securableType")
    def securable_type(self) -> pulumi.Output[Optional[str]]:
        """
        Type of securable. Can be `catalog`, `external-location` or `storage-credential`. Default to `catalog`. Change forces creation of a new resource.
        """
        return pulumi.get(self, "securable_type")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Output[Optional[str]]:
        """
        ID of the workspace. Change forces creation of a new resource.
        """
        return pulumi.get(self, "workspace_id")

