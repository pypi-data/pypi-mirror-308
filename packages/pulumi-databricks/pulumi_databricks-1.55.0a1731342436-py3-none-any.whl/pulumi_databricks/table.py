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
from . import outputs
from ._inputs import *

__all__ = ['TableArgs', 'Table']

@pulumi.input_type
class TableArgs:
    def __init__(__self__, *,
                 catalog_name: pulumi.Input[str],
                 columns: pulumi.Input[Sequence[pulumi.Input['TableColumnArgs']]],
                 data_source_format: pulumi.Input[str],
                 schema_name: pulumi.Input[str],
                 table_type: pulumi.Input[str],
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 storage_credential_name: Optional[pulumi.Input[str]] = None,
                 storage_location: Optional[pulumi.Input[str]] = None,
                 view_definition: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Table resource.
        """
        pulumi.set(__self__, "catalog_name", catalog_name)
        pulumi.set(__self__, "columns", columns)
        pulumi.set(__self__, "data_source_format", data_source_format)
        pulumi.set(__self__, "schema_name", schema_name)
        pulumi.set(__self__, "table_type", table_type)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if owner is not None:
            pulumi.set(__self__, "owner", owner)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if storage_credential_name is not None:
            pulumi.set(__self__, "storage_credential_name", storage_credential_name)
        if storage_location is not None:
            pulumi.set(__self__, "storage_location", storage_location)
        if view_definition is not None:
            pulumi.set(__self__, "view_definition", view_definition)

    @property
    @pulumi.getter(name="catalogName")
    def catalog_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "catalog_name")

    @catalog_name.setter
    def catalog_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "catalog_name", value)

    @property
    @pulumi.getter
    def columns(self) -> pulumi.Input[Sequence[pulumi.Input['TableColumnArgs']]]:
        return pulumi.get(self, "columns")

    @columns.setter
    def columns(self, value: pulumi.Input[Sequence[pulumi.Input['TableColumnArgs']]]):
        pulumi.set(self, "columns", value)

    @property
    @pulumi.getter(name="dataSourceFormat")
    def data_source_format(self) -> pulumi.Input[str]:
        return pulumi.get(self, "data_source_format")

    @data_source_format.setter
    def data_source_format(self, value: pulumi.Input[str]):
        pulumi.set(self, "data_source_format", value)

    @property
    @pulumi.getter(name="schemaName")
    def schema_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "schema_name")

    @schema_name.setter
    def schema_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "schema_name", value)

    @property
    @pulumi.getter(name="tableType")
    def table_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "table_type")

    @table_type.setter
    def table_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "table_type", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def owner(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "owner")

    @owner.setter
    def owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="storageCredentialName")
    def storage_credential_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "storage_credential_name")

    @storage_credential_name.setter
    def storage_credential_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_credential_name", value)

    @property
    @pulumi.getter(name="storageLocation")
    def storage_location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "storage_location")

    @storage_location.setter
    def storage_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_location", value)

    @property
    @pulumi.getter(name="viewDefinition")
    def view_definition(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "view_definition")

    @view_definition.setter
    def view_definition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "view_definition", value)


@pulumi.input_type
class _TableState:
    def __init__(__self__, *,
                 catalog_name: Optional[pulumi.Input[str]] = None,
                 columns: Optional[pulumi.Input[Sequence[pulumi.Input['TableColumnArgs']]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 data_source_format: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 schema_name: Optional[pulumi.Input[str]] = None,
                 storage_credential_name: Optional[pulumi.Input[str]] = None,
                 storage_location: Optional[pulumi.Input[str]] = None,
                 table_type: Optional[pulumi.Input[str]] = None,
                 view_definition: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Table resources.
        """
        if catalog_name is not None:
            pulumi.set(__self__, "catalog_name", catalog_name)
        if columns is not None:
            pulumi.set(__self__, "columns", columns)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if data_source_format is not None:
            pulumi.set(__self__, "data_source_format", data_source_format)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if owner is not None:
            pulumi.set(__self__, "owner", owner)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if schema_name is not None:
            pulumi.set(__self__, "schema_name", schema_name)
        if storage_credential_name is not None:
            pulumi.set(__self__, "storage_credential_name", storage_credential_name)
        if storage_location is not None:
            pulumi.set(__self__, "storage_location", storage_location)
        if table_type is not None:
            pulumi.set(__self__, "table_type", table_type)
        if view_definition is not None:
            pulumi.set(__self__, "view_definition", view_definition)

    @property
    @pulumi.getter(name="catalogName")
    def catalog_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "catalog_name")

    @catalog_name.setter
    def catalog_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "catalog_name", value)

    @property
    @pulumi.getter
    def columns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TableColumnArgs']]]]:
        return pulumi.get(self, "columns")

    @columns.setter
    def columns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TableColumnArgs']]]]):
        pulumi.set(self, "columns", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="dataSourceFormat")
    def data_source_format(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "data_source_format")

    @data_source_format.setter
    def data_source_format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_source_format", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def owner(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "owner")

    @owner.setter
    def owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="schemaName")
    def schema_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "schema_name")

    @schema_name.setter
    def schema_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schema_name", value)

    @property
    @pulumi.getter(name="storageCredentialName")
    def storage_credential_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "storage_credential_name")

    @storage_credential_name.setter
    def storage_credential_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_credential_name", value)

    @property
    @pulumi.getter(name="storageLocation")
    def storage_location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "storage_location")

    @storage_location.setter
    def storage_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_location", value)

    @property
    @pulumi.getter(name="tableType")
    def table_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "table_type")

    @table_type.setter
    def table_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "table_type", value)

    @property
    @pulumi.getter(name="viewDefinition")
    def view_definition(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "view_definition")

    @view_definition.setter
    def view_definition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "view_definition", value)


class Table(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 catalog_name: Optional[pulumi.Input[str]] = None,
                 columns: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TableColumnArgs', 'TableColumnArgsDict']]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 data_source_format: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 schema_name: Optional[pulumi.Input[str]] = None,
                 storage_credential_name: Optional[pulumi.Input[str]] = None,
                 storage_location: Optional[pulumi.Input[str]] = None,
                 table_type: Optional[pulumi.Input[str]] = None,
                 view_definition: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a Table resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TableArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Table resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param TableArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TableArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 catalog_name: Optional[pulumi.Input[str]] = None,
                 columns: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TableColumnArgs', 'TableColumnArgsDict']]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 data_source_format: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 schema_name: Optional[pulumi.Input[str]] = None,
                 storage_credential_name: Optional[pulumi.Input[str]] = None,
                 storage_location: Optional[pulumi.Input[str]] = None,
                 table_type: Optional[pulumi.Input[str]] = None,
                 view_definition: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TableArgs.__new__(TableArgs)

            if catalog_name is None and not opts.urn:
                raise TypeError("Missing required property 'catalog_name'")
            __props__.__dict__["catalog_name"] = catalog_name
            if columns is None and not opts.urn:
                raise TypeError("Missing required property 'columns'")
            __props__.__dict__["columns"] = columns
            __props__.__dict__["comment"] = comment
            if data_source_format is None and not opts.urn:
                raise TypeError("Missing required property 'data_source_format'")
            __props__.__dict__["data_source_format"] = data_source_format
            __props__.__dict__["name"] = name
            __props__.__dict__["owner"] = owner
            __props__.__dict__["properties"] = properties
            if schema_name is None and not opts.urn:
                raise TypeError("Missing required property 'schema_name'")
            __props__.__dict__["schema_name"] = schema_name
            __props__.__dict__["storage_credential_name"] = storage_credential_name
            __props__.__dict__["storage_location"] = storage_location
            if table_type is None and not opts.urn:
                raise TypeError("Missing required property 'table_type'")
            __props__.__dict__["table_type"] = table_type
            __props__.__dict__["view_definition"] = view_definition
        super(Table, __self__).__init__(
            'databricks:index/table:Table',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            catalog_name: Optional[pulumi.Input[str]] = None,
            columns: Optional[pulumi.Input[Sequence[pulumi.Input[Union['TableColumnArgs', 'TableColumnArgsDict']]]]] = None,
            comment: Optional[pulumi.Input[str]] = None,
            data_source_format: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            owner: Optional[pulumi.Input[str]] = None,
            properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            schema_name: Optional[pulumi.Input[str]] = None,
            storage_credential_name: Optional[pulumi.Input[str]] = None,
            storage_location: Optional[pulumi.Input[str]] = None,
            table_type: Optional[pulumi.Input[str]] = None,
            view_definition: Optional[pulumi.Input[str]] = None) -> 'Table':
        """
        Get an existing Table resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TableState.__new__(_TableState)

        __props__.__dict__["catalog_name"] = catalog_name
        __props__.__dict__["columns"] = columns
        __props__.__dict__["comment"] = comment
        __props__.__dict__["data_source_format"] = data_source_format
        __props__.__dict__["name"] = name
        __props__.__dict__["owner"] = owner
        __props__.__dict__["properties"] = properties
        __props__.__dict__["schema_name"] = schema_name
        __props__.__dict__["storage_credential_name"] = storage_credential_name
        __props__.__dict__["storage_location"] = storage_location
        __props__.__dict__["table_type"] = table_type
        __props__.__dict__["view_definition"] = view_definition
        return Table(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="catalogName")
    def catalog_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "catalog_name")

    @property
    @pulumi.getter
    def columns(self) -> pulumi.Output[Sequence['outputs.TableColumn']]:
        return pulumi.get(self, "columns")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter(name="dataSourceFormat")
    def data_source_format(self) -> pulumi.Output[str]:
        return pulumi.get(self, "data_source_format")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def owner(self) -> pulumi.Output[str]:
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="schemaName")
    def schema_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "schema_name")

    @property
    @pulumi.getter(name="storageCredentialName")
    def storage_credential_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "storage_credential_name")

    @property
    @pulumi.getter(name="storageLocation")
    def storage_location(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "storage_location")

    @property
    @pulumi.getter(name="tableType")
    def table_type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "table_type")

    @property
    @pulumi.getter(name="viewDefinition")
    def view_definition(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "view_definition")

