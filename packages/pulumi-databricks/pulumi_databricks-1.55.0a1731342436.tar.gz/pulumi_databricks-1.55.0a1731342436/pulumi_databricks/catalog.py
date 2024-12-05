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

__all__ = ['CatalogArgs', 'Catalog']

@pulumi.input_type
class CatalogArgs:
    def __init__(__self__, *,
                 comment: Optional[pulumi.Input[str]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_predictive_optimization: Optional[pulumi.Input[str]] = None,
                 force_destroy: Optional[pulumi.Input[bool]] = None,
                 isolation_mode: Optional[pulumi.Input[str]] = None,
                 metastore_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 storage_root: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Catalog resource.
        :param pulumi.Input[str] comment: User-supplied free-form text.
        :param pulumi.Input[str] connection_name: For Foreign Catalogs: the name of the connection to an external data source. Changes forces creation of a new resource.
        :param pulumi.Input[str] enable_predictive_optimization: Whether predictive optimization should be enabled for this object and objects under it. Can be `ENABLE`, `DISABLE` or `INHERIT`
        :param pulumi.Input[bool] force_destroy: Delete catalog regardless of its contents.
        :param pulumi.Input[str] isolation_mode: Whether the catalog is accessible from all workspaces or a specific set of workspaces. Can be `ISOLATED` or `OPEN`. Setting the catalog to `ISOLATED` will automatically allow access from the current workspace.
        :param pulumi.Input[str] metastore_id: ID of the parent metastore.
        :param pulumi.Input[str] name: Name of Catalog relative to parent metastore.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: For Foreign Catalogs: the name of the entity from an external data source that maps to a catalog. For example, the database name in a PostgreSQL server.
        :param pulumi.Input[str] owner: Username/groupname/sp application_id of the catalog owner.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] properties: Extensible Catalog properties.
        :param pulumi.Input[str] provider_name: For Delta Sharing Catalogs: the name of the delta sharing provider. Change forces creation of a new resource.
        :param pulumi.Input[str] share_name: For Delta Sharing Catalogs: the name of the share under the share provider. Change forces creation of a new resource.
        :param pulumi.Input[str] storage_root: Managed location of the catalog. Location in cloud storage where data for managed tables will be stored. If not specified, the location will default to the metastore root location. Change forces creation of a new resource.
        """
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if connection_name is not None:
            pulumi.set(__self__, "connection_name", connection_name)
        if enable_predictive_optimization is not None:
            pulumi.set(__self__, "enable_predictive_optimization", enable_predictive_optimization)
        if force_destroy is not None:
            pulumi.set(__self__, "force_destroy", force_destroy)
        if isolation_mode is not None:
            pulumi.set(__self__, "isolation_mode", isolation_mode)
        if metastore_id is not None:
            pulumi.set(__self__, "metastore_id", metastore_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if options is not None:
            pulumi.set(__self__, "options", options)
        if owner is not None:
            pulumi.set(__self__, "owner", owner)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if provider_name is not None:
            pulumi.set(__self__, "provider_name", provider_name)
        if share_name is not None:
            pulumi.set(__self__, "share_name", share_name)
        if storage_root is not None:
            pulumi.set(__self__, "storage_root", storage_root)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        User-supplied free-form text.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="connectionName")
    def connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        For Foreign Catalogs: the name of the connection to an external data source. Changes forces creation of a new resource.
        """
        return pulumi.get(self, "connection_name")

    @connection_name.setter
    def connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_name", value)

    @property
    @pulumi.getter(name="enablePredictiveOptimization")
    def enable_predictive_optimization(self) -> Optional[pulumi.Input[str]]:
        """
        Whether predictive optimization should be enabled for this object and objects under it. Can be `ENABLE`, `DISABLE` or `INHERIT`
        """
        return pulumi.get(self, "enable_predictive_optimization")

    @enable_predictive_optimization.setter
    def enable_predictive_optimization(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "enable_predictive_optimization", value)

    @property
    @pulumi.getter(name="forceDestroy")
    def force_destroy(self) -> Optional[pulumi.Input[bool]]:
        """
        Delete catalog regardless of its contents.
        """
        return pulumi.get(self, "force_destroy")

    @force_destroy.setter
    def force_destroy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force_destroy", value)

    @property
    @pulumi.getter(name="isolationMode")
    def isolation_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Whether the catalog is accessible from all workspaces or a specific set of workspaces. Can be `ISOLATED` or `OPEN`. Setting the catalog to `ISOLATED` will automatically allow access from the current workspace.
        """
        return pulumi.get(self, "isolation_mode")

    @isolation_mode.setter
    def isolation_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "isolation_mode", value)

    @property
    @pulumi.getter(name="metastoreId")
    def metastore_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the parent metastore.
        """
        return pulumi.get(self, "metastore_id")

    @metastore_id.setter
    def metastore_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metastore_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of Catalog relative to parent metastore.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def options(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        For Foreign Catalogs: the name of the entity from an external data source that maps to a catalog. For example, the database name in a PostgreSQL server.
        """
        return pulumi.get(self, "options")

    @options.setter
    def options(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "options", value)

    @property
    @pulumi.getter
    def owner(self) -> Optional[pulumi.Input[str]]:
        """
        Username/groupname/sp application_id of the catalog owner.
        """
        return pulumi.get(self, "owner")

    @owner.setter
    def owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Extensible Catalog properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="providerName")
    def provider_name(self) -> Optional[pulumi.Input[str]]:
        """
        For Delta Sharing Catalogs: the name of the delta sharing provider. Change forces creation of a new resource.
        """
        return pulumi.get(self, "provider_name")

    @provider_name.setter
    def provider_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provider_name", value)

    @property
    @pulumi.getter(name="shareName")
    def share_name(self) -> Optional[pulumi.Input[str]]:
        """
        For Delta Sharing Catalogs: the name of the share under the share provider. Change forces creation of a new resource.
        """
        return pulumi.get(self, "share_name")

    @share_name.setter
    def share_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "share_name", value)

    @property
    @pulumi.getter(name="storageRoot")
    def storage_root(self) -> Optional[pulumi.Input[str]]:
        """
        Managed location of the catalog. Location in cloud storage where data for managed tables will be stored. If not specified, the location will default to the metastore root location. Change forces creation of a new resource.
        """
        return pulumi.get(self, "storage_root")

    @storage_root.setter
    def storage_root(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_root", value)


@pulumi.input_type
class _CatalogState:
    def __init__(__self__, *,
                 comment: Optional[pulumi.Input[str]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_predictive_optimization: Optional[pulumi.Input[str]] = None,
                 force_destroy: Optional[pulumi.Input[bool]] = None,
                 isolation_mode: Optional[pulumi.Input[str]] = None,
                 metastore_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 storage_root: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Catalog resources.
        :param pulumi.Input[str] comment: User-supplied free-form text.
        :param pulumi.Input[str] connection_name: For Foreign Catalogs: the name of the connection to an external data source. Changes forces creation of a new resource.
        :param pulumi.Input[str] enable_predictive_optimization: Whether predictive optimization should be enabled for this object and objects under it. Can be `ENABLE`, `DISABLE` or `INHERIT`
        :param pulumi.Input[bool] force_destroy: Delete catalog regardless of its contents.
        :param pulumi.Input[str] isolation_mode: Whether the catalog is accessible from all workspaces or a specific set of workspaces. Can be `ISOLATED` or `OPEN`. Setting the catalog to `ISOLATED` will automatically allow access from the current workspace.
        :param pulumi.Input[str] metastore_id: ID of the parent metastore.
        :param pulumi.Input[str] name: Name of Catalog relative to parent metastore.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: For Foreign Catalogs: the name of the entity from an external data source that maps to a catalog. For example, the database name in a PostgreSQL server.
        :param pulumi.Input[str] owner: Username/groupname/sp application_id of the catalog owner.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] properties: Extensible Catalog properties.
        :param pulumi.Input[str] provider_name: For Delta Sharing Catalogs: the name of the delta sharing provider. Change forces creation of a new resource.
        :param pulumi.Input[str] share_name: For Delta Sharing Catalogs: the name of the share under the share provider. Change forces creation of a new resource.
        :param pulumi.Input[str] storage_root: Managed location of the catalog. Location in cloud storage where data for managed tables will be stored. If not specified, the location will default to the metastore root location. Change forces creation of a new resource.
        """
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if connection_name is not None:
            pulumi.set(__self__, "connection_name", connection_name)
        if enable_predictive_optimization is not None:
            pulumi.set(__self__, "enable_predictive_optimization", enable_predictive_optimization)
        if force_destroy is not None:
            pulumi.set(__self__, "force_destroy", force_destroy)
        if isolation_mode is not None:
            pulumi.set(__self__, "isolation_mode", isolation_mode)
        if metastore_id is not None:
            pulumi.set(__self__, "metastore_id", metastore_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if options is not None:
            pulumi.set(__self__, "options", options)
        if owner is not None:
            pulumi.set(__self__, "owner", owner)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if provider_name is not None:
            pulumi.set(__self__, "provider_name", provider_name)
        if share_name is not None:
            pulumi.set(__self__, "share_name", share_name)
        if storage_root is not None:
            pulumi.set(__self__, "storage_root", storage_root)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        User-supplied free-form text.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="connectionName")
    def connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        For Foreign Catalogs: the name of the connection to an external data source. Changes forces creation of a new resource.
        """
        return pulumi.get(self, "connection_name")

    @connection_name.setter
    def connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_name", value)

    @property
    @pulumi.getter(name="enablePredictiveOptimization")
    def enable_predictive_optimization(self) -> Optional[pulumi.Input[str]]:
        """
        Whether predictive optimization should be enabled for this object and objects under it. Can be `ENABLE`, `DISABLE` or `INHERIT`
        """
        return pulumi.get(self, "enable_predictive_optimization")

    @enable_predictive_optimization.setter
    def enable_predictive_optimization(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "enable_predictive_optimization", value)

    @property
    @pulumi.getter(name="forceDestroy")
    def force_destroy(self) -> Optional[pulumi.Input[bool]]:
        """
        Delete catalog regardless of its contents.
        """
        return pulumi.get(self, "force_destroy")

    @force_destroy.setter
    def force_destroy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force_destroy", value)

    @property
    @pulumi.getter(name="isolationMode")
    def isolation_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Whether the catalog is accessible from all workspaces or a specific set of workspaces. Can be `ISOLATED` or `OPEN`. Setting the catalog to `ISOLATED` will automatically allow access from the current workspace.
        """
        return pulumi.get(self, "isolation_mode")

    @isolation_mode.setter
    def isolation_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "isolation_mode", value)

    @property
    @pulumi.getter(name="metastoreId")
    def metastore_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the parent metastore.
        """
        return pulumi.get(self, "metastore_id")

    @metastore_id.setter
    def metastore_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metastore_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of Catalog relative to parent metastore.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def options(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        For Foreign Catalogs: the name of the entity from an external data source that maps to a catalog. For example, the database name in a PostgreSQL server.
        """
        return pulumi.get(self, "options")

    @options.setter
    def options(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "options", value)

    @property
    @pulumi.getter
    def owner(self) -> Optional[pulumi.Input[str]]:
        """
        Username/groupname/sp application_id of the catalog owner.
        """
        return pulumi.get(self, "owner")

    @owner.setter
    def owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Extensible Catalog properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="providerName")
    def provider_name(self) -> Optional[pulumi.Input[str]]:
        """
        For Delta Sharing Catalogs: the name of the delta sharing provider. Change forces creation of a new resource.
        """
        return pulumi.get(self, "provider_name")

    @provider_name.setter
    def provider_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provider_name", value)

    @property
    @pulumi.getter(name="shareName")
    def share_name(self) -> Optional[pulumi.Input[str]]:
        """
        For Delta Sharing Catalogs: the name of the share under the share provider. Change forces creation of a new resource.
        """
        return pulumi.get(self, "share_name")

    @share_name.setter
    def share_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "share_name", value)

    @property
    @pulumi.getter(name="storageRoot")
    def storage_root(self) -> Optional[pulumi.Input[str]]:
        """
        Managed location of the catalog. Location in cloud storage where data for managed tables will be stored. If not specified, the location will default to the metastore root location. Change forces creation of a new resource.
        """
        return pulumi.get(self, "storage_root")

    @storage_root.setter
    def storage_root(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_root", value)


class Catalog(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_predictive_optimization: Optional[pulumi.Input[str]] = None,
                 force_destroy: Optional[pulumi.Input[bool]] = None,
                 isolation_mode: Optional[pulumi.Input[str]] = None,
                 metastore_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 storage_root: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        > This resource can only be used with a workspace-level provider!

        Within a metastore, Unity Catalog provides a 3-level namespace for organizing data: Catalogs, Databases (also called Schemas), and Tables / Views.

        A `Catalog` is contained within Metastore and can contain databricks_schema. By default, Databricks creates `default` schema for every new catalog, but Pulumi plugin is removing this auto-created schema, so that resource destruction could be done in a clean way.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_databricks as databricks

        sandbox = databricks.Catalog("sandbox",
            name="sandbox",
            comment="this catalog is managed by terraform",
            properties={
                "purpose": "testing",
            })
        ```

        ## Related Resources

        The following resources are used in the same context:

        * get_tables data to list tables within Unity Catalog.
        * get_schemas data to list schemas within Unity Catalog.
        * get_catalogs data to list catalogs within Unity Catalog.

        ## Import

        This resource can be imported by name:

        bash

        ```sh
        $ pulumi import databricks:index/catalog:Catalog this <name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] comment: User-supplied free-form text.
        :param pulumi.Input[str] connection_name: For Foreign Catalogs: the name of the connection to an external data source. Changes forces creation of a new resource.
        :param pulumi.Input[str] enable_predictive_optimization: Whether predictive optimization should be enabled for this object and objects under it. Can be `ENABLE`, `DISABLE` or `INHERIT`
        :param pulumi.Input[bool] force_destroy: Delete catalog regardless of its contents.
        :param pulumi.Input[str] isolation_mode: Whether the catalog is accessible from all workspaces or a specific set of workspaces. Can be `ISOLATED` or `OPEN`. Setting the catalog to `ISOLATED` will automatically allow access from the current workspace.
        :param pulumi.Input[str] metastore_id: ID of the parent metastore.
        :param pulumi.Input[str] name: Name of Catalog relative to parent metastore.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: For Foreign Catalogs: the name of the entity from an external data source that maps to a catalog. For example, the database name in a PostgreSQL server.
        :param pulumi.Input[str] owner: Username/groupname/sp application_id of the catalog owner.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] properties: Extensible Catalog properties.
        :param pulumi.Input[str] provider_name: For Delta Sharing Catalogs: the name of the delta sharing provider. Change forces creation of a new resource.
        :param pulumi.Input[str] share_name: For Delta Sharing Catalogs: the name of the share under the share provider. Change forces creation of a new resource.
        :param pulumi.Input[str] storage_root: Managed location of the catalog. Location in cloud storage where data for managed tables will be stored. If not specified, the location will default to the metastore root location. Change forces creation of a new resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[CatalogArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        > This resource can only be used with a workspace-level provider!

        Within a metastore, Unity Catalog provides a 3-level namespace for organizing data: Catalogs, Databases (also called Schemas), and Tables / Views.

        A `Catalog` is contained within Metastore and can contain databricks_schema. By default, Databricks creates `default` schema for every new catalog, but Pulumi plugin is removing this auto-created schema, so that resource destruction could be done in a clean way.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_databricks as databricks

        sandbox = databricks.Catalog("sandbox",
            name="sandbox",
            comment="this catalog is managed by terraform",
            properties={
                "purpose": "testing",
            })
        ```

        ## Related Resources

        The following resources are used in the same context:

        * get_tables data to list tables within Unity Catalog.
        * get_schemas data to list schemas within Unity Catalog.
        * get_catalogs data to list catalogs within Unity Catalog.

        ## Import

        This resource can be imported by name:

        bash

        ```sh
        $ pulumi import databricks:index/catalog:Catalog this <name>
        ```

        :param str resource_name: The name of the resource.
        :param CatalogArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CatalogArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_predictive_optimization: Optional[pulumi.Input[str]] = None,
                 force_destroy: Optional[pulumi.Input[bool]] = None,
                 isolation_mode: Optional[pulumi.Input[str]] = None,
                 metastore_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 storage_root: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CatalogArgs.__new__(CatalogArgs)

            __props__.__dict__["comment"] = comment
            __props__.__dict__["connection_name"] = connection_name
            __props__.__dict__["enable_predictive_optimization"] = enable_predictive_optimization
            __props__.__dict__["force_destroy"] = force_destroy
            __props__.__dict__["isolation_mode"] = isolation_mode
            __props__.__dict__["metastore_id"] = metastore_id
            __props__.__dict__["name"] = name
            __props__.__dict__["options"] = options
            __props__.__dict__["owner"] = owner
            __props__.__dict__["properties"] = properties
            __props__.__dict__["provider_name"] = provider_name
            __props__.__dict__["share_name"] = share_name
            __props__.__dict__["storage_root"] = storage_root
        super(Catalog, __self__).__init__(
            'databricks:index/catalog:Catalog',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            comment: Optional[pulumi.Input[str]] = None,
            connection_name: Optional[pulumi.Input[str]] = None,
            enable_predictive_optimization: Optional[pulumi.Input[str]] = None,
            force_destroy: Optional[pulumi.Input[bool]] = None,
            isolation_mode: Optional[pulumi.Input[str]] = None,
            metastore_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            owner: Optional[pulumi.Input[str]] = None,
            properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            provider_name: Optional[pulumi.Input[str]] = None,
            share_name: Optional[pulumi.Input[str]] = None,
            storage_root: Optional[pulumi.Input[str]] = None) -> 'Catalog':
        """
        Get an existing Catalog resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] comment: User-supplied free-form text.
        :param pulumi.Input[str] connection_name: For Foreign Catalogs: the name of the connection to an external data source. Changes forces creation of a new resource.
        :param pulumi.Input[str] enable_predictive_optimization: Whether predictive optimization should be enabled for this object and objects under it. Can be `ENABLE`, `DISABLE` or `INHERIT`
        :param pulumi.Input[bool] force_destroy: Delete catalog regardless of its contents.
        :param pulumi.Input[str] isolation_mode: Whether the catalog is accessible from all workspaces or a specific set of workspaces. Can be `ISOLATED` or `OPEN`. Setting the catalog to `ISOLATED` will automatically allow access from the current workspace.
        :param pulumi.Input[str] metastore_id: ID of the parent metastore.
        :param pulumi.Input[str] name: Name of Catalog relative to parent metastore.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: For Foreign Catalogs: the name of the entity from an external data source that maps to a catalog. For example, the database name in a PostgreSQL server.
        :param pulumi.Input[str] owner: Username/groupname/sp application_id of the catalog owner.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] properties: Extensible Catalog properties.
        :param pulumi.Input[str] provider_name: For Delta Sharing Catalogs: the name of the delta sharing provider. Change forces creation of a new resource.
        :param pulumi.Input[str] share_name: For Delta Sharing Catalogs: the name of the share under the share provider. Change forces creation of a new resource.
        :param pulumi.Input[str] storage_root: Managed location of the catalog. Location in cloud storage where data for managed tables will be stored. If not specified, the location will default to the metastore root location. Change forces creation of a new resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CatalogState.__new__(_CatalogState)

        __props__.__dict__["comment"] = comment
        __props__.__dict__["connection_name"] = connection_name
        __props__.__dict__["enable_predictive_optimization"] = enable_predictive_optimization
        __props__.__dict__["force_destroy"] = force_destroy
        __props__.__dict__["isolation_mode"] = isolation_mode
        __props__.__dict__["metastore_id"] = metastore_id
        __props__.__dict__["name"] = name
        __props__.__dict__["options"] = options
        __props__.__dict__["owner"] = owner
        __props__.__dict__["properties"] = properties
        __props__.__dict__["provider_name"] = provider_name
        __props__.__dict__["share_name"] = share_name
        __props__.__dict__["storage_root"] = storage_root
        return Catalog(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        User-supplied free-form text.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter(name="connectionName")
    def connection_name(self) -> pulumi.Output[Optional[str]]:
        """
        For Foreign Catalogs: the name of the connection to an external data source. Changes forces creation of a new resource.
        """
        return pulumi.get(self, "connection_name")

    @property
    @pulumi.getter(name="enablePredictiveOptimization")
    def enable_predictive_optimization(self) -> pulumi.Output[str]:
        """
        Whether predictive optimization should be enabled for this object and objects under it. Can be `ENABLE`, `DISABLE` or `INHERIT`
        """
        return pulumi.get(self, "enable_predictive_optimization")

    @property
    @pulumi.getter(name="forceDestroy")
    def force_destroy(self) -> pulumi.Output[Optional[bool]]:
        """
        Delete catalog regardless of its contents.
        """
        return pulumi.get(self, "force_destroy")

    @property
    @pulumi.getter(name="isolationMode")
    def isolation_mode(self) -> pulumi.Output[str]:
        """
        Whether the catalog is accessible from all workspaces or a specific set of workspaces. Can be `ISOLATED` or `OPEN`. Setting the catalog to `ISOLATED` will automatically allow access from the current workspace.
        """
        return pulumi.get(self, "isolation_mode")

    @property
    @pulumi.getter(name="metastoreId")
    def metastore_id(self) -> pulumi.Output[str]:
        """
        ID of the parent metastore.
        """
        return pulumi.get(self, "metastore_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of Catalog relative to parent metastore.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def options(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        For Foreign Catalogs: the name of the entity from an external data source that maps to a catalog. For example, the database name in a PostgreSQL server.
        """
        return pulumi.get(self, "options")

    @property
    @pulumi.getter
    def owner(self) -> pulumi.Output[str]:
        """
        Username/groupname/sp application_id of the catalog owner.
        """
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Extensible Catalog properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="providerName")
    def provider_name(self) -> pulumi.Output[Optional[str]]:
        """
        For Delta Sharing Catalogs: the name of the delta sharing provider. Change forces creation of a new resource.
        """
        return pulumi.get(self, "provider_name")

    @property
    @pulumi.getter(name="shareName")
    def share_name(self) -> pulumi.Output[Optional[str]]:
        """
        For Delta Sharing Catalogs: the name of the share under the share provider. Change forces creation of a new resource.
        """
        return pulumi.get(self, "share_name")

    @property
    @pulumi.getter(name="storageRoot")
    def storage_root(self) -> pulumi.Output[Optional[str]]:
        """
        Managed location of the catalog. Location in cloud storage where data for managed tables will be stored. If not specified, the location will default to the metastore root location. Change forces creation of a new resource.
        """
        return pulumi.get(self, "storage_root")

