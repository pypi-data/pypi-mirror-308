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

__all__ = [
    'GetSchemaResult',
    'AwaitableGetSchemaResult',
    'get_schema',
    'get_schema_output',
]

@pulumi.output_type
class GetSchemaResult:
    """
    A collection of values returned by getSchema.
    """
    def __init__(__self__, id=None, name=None, schema_info=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if schema_info and not isinstance(schema_info, dict):
            raise TypeError("Expected argument 'schema_info' to be a dict")
        pulumi.set(__self__, "schema_info", schema_info)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of this Unity Catalog Schema in form of `<catalog>.<schema>`.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of schema, relative to parent catalog.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="schemaInfo")
    def schema_info(self) -> 'outputs.GetSchemaSchemaInfoResult':
        """
        `SchemaInfo` object for a Unity Catalog schema. This contains the following attributes:
        """
        return pulumi.get(self, "schema_info")


class AwaitableGetSchemaResult(GetSchemaResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSchemaResult(
            id=self.id,
            name=self.name,
            schema_info=self.schema_info)


def get_schema(id: Optional[str] = None,
               name: Optional[str] = None,
               schema_info: Optional[Union['GetSchemaSchemaInfoArgs', 'GetSchemaSchemaInfoArgsDict']] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSchemaResult:
    """
    Retrieves details about Schema that was created by Pulumi or manually.
    A schema can be identified by its two-level (fully qualified) name (in the form of: `catalog_name`.`schema_name`) as input. This can be retrieved programmatically using get_schemas data source.

    ## Example Usage

    * Retrieve details of all schemas in in a _sandbox_ databricks_catalog:

    ```python
    import pulumi
    import pulumi_databricks as databricks

    all = databricks.get_schemas(catalog_name="sandbox")
    this = {__key: databricks.get_schema(name=__value) for __key, __value in all.ids}
    ```

    * Search for a specific schema by its fully qualified name:

    ```python
    import pulumi
    import pulumi_databricks as databricks

    this = databricks.get_schema(name="catalog.schema")
    ```

    ## Related Resources

    The following resources are used in the same context:

    * Schema to manage schemas within Unity Catalog.
    * Catalog to manage catalogs within Unity Catalog.


    :param str id: ID of this Unity Catalog Schema in form of `<catalog>.<schema>`.
    :param str name: a fully qualified name of databricks_schema: *`catalog`.`schema`*
    :param Union['GetSchemaSchemaInfoArgs', 'GetSchemaSchemaInfoArgsDict'] schema_info: `SchemaInfo` object for a Unity Catalog schema. This contains the following attributes:
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['name'] = name
    __args__['schemaInfo'] = schema_info
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('databricks:index/getSchema:getSchema', __args__, opts=opts, typ=GetSchemaResult).value

    return AwaitableGetSchemaResult(
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        schema_info=pulumi.get(__ret__, 'schema_info'))
def get_schema_output(id: Optional[pulumi.Input[Optional[str]]] = None,
                      name: Optional[pulumi.Input[str]] = None,
                      schema_info: Optional[pulumi.Input[Optional[Union['GetSchemaSchemaInfoArgs', 'GetSchemaSchemaInfoArgsDict']]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSchemaResult]:
    """
    Retrieves details about Schema that was created by Pulumi or manually.
    A schema can be identified by its two-level (fully qualified) name (in the form of: `catalog_name`.`schema_name`) as input. This can be retrieved programmatically using get_schemas data source.

    ## Example Usage

    * Retrieve details of all schemas in in a _sandbox_ databricks_catalog:

    ```python
    import pulumi
    import pulumi_databricks as databricks

    all = databricks.get_schemas(catalog_name="sandbox")
    this = {__key: databricks.get_schema(name=__value) for __key, __value in all.ids}
    ```

    * Search for a specific schema by its fully qualified name:

    ```python
    import pulumi
    import pulumi_databricks as databricks

    this = databricks.get_schema(name="catalog.schema")
    ```

    ## Related Resources

    The following resources are used in the same context:

    * Schema to manage schemas within Unity Catalog.
    * Catalog to manage catalogs within Unity Catalog.


    :param str id: ID of this Unity Catalog Schema in form of `<catalog>.<schema>`.
    :param str name: a fully qualified name of databricks_schema: *`catalog`.`schema`*
    :param Union['GetSchemaSchemaInfoArgs', 'GetSchemaSchemaInfoArgsDict'] schema_info: `SchemaInfo` object for a Unity Catalog schema. This contains the following attributes:
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['name'] = name
    __args__['schemaInfo'] = schema_info
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('databricks:index/getSchema:getSchema', __args__, opts=opts, typ=GetSchemaResult)
    return __ret__.apply(lambda __response__: GetSchemaResult(
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        schema_info=pulumi.get(__response__, 'schema_info')))
