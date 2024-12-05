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

__all__ = ['VectorSearchEndpointArgs', 'VectorSearchEndpoint']

@pulumi.input_type
class VectorSearchEndpointArgs:
    def __init__(__self__, *,
                 endpoint_type: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a VectorSearchEndpoint resource.
        :param pulumi.Input[str] endpoint_type: Type of Mosaic AI Vector Search Endpoint.  Currently only accepting single value: `STANDARD` (See [documentation](https://docs.databricks.com/api/workspace/vectorsearchendpoints/createendpoint) for the list of currently supported values).
        :param pulumi.Input[str] name: Name of the Mosaic AI Vector Search Endpoint to create.
        """
        pulumi.set(__self__, "endpoint_type", endpoint_type)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> pulumi.Input[str]:
        """
        Type of Mosaic AI Vector Search Endpoint.  Currently only accepting single value: `STANDARD` (See [documentation](https://docs.databricks.com/api/workspace/vectorsearchendpoints/createendpoint) for the list of currently supported values).
        """
        return pulumi.get(self, "endpoint_type")

    @endpoint_type.setter
    def endpoint_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "endpoint_type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Mosaic AI Vector Search Endpoint to create.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _VectorSearchEndpointState:
    def __init__(__self__, *,
                 creation_timestamp: Optional[pulumi.Input[int]] = None,
                 creator: Optional[pulumi.Input[str]] = None,
                 endpoint_id: Optional[pulumi.Input[str]] = None,
                 endpoint_statuses: Optional[pulumi.Input[Sequence[pulumi.Input['VectorSearchEndpointEndpointStatusArgs']]]] = None,
                 endpoint_type: Optional[pulumi.Input[str]] = None,
                 last_updated_timestamp: Optional[pulumi.Input[int]] = None,
                 last_updated_user: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 num_indexes: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering VectorSearchEndpoint resources.
        :param pulumi.Input[int] creation_timestamp: Timestamp of endpoint creation (milliseconds).
        :param pulumi.Input[str] creator: Creator of the endpoint.
        :param pulumi.Input[str] endpoint_id: Unique internal identifier of the endpoint (UUID).
        :param pulumi.Input[Sequence[pulumi.Input['VectorSearchEndpointEndpointStatusArgs']]] endpoint_statuses: Object describing the current status of the endpoint consisting of the following fields:
        :param pulumi.Input[str] endpoint_type: Type of Mosaic AI Vector Search Endpoint.  Currently only accepting single value: `STANDARD` (See [documentation](https://docs.databricks.com/api/workspace/vectorsearchendpoints/createendpoint) for the list of currently supported values).
        :param pulumi.Input[int] last_updated_timestamp: Timestamp of the last update to the endpoint (milliseconds).
        :param pulumi.Input[str] last_updated_user: User who last updated the endpoint.
        :param pulumi.Input[str] name: Name of the Mosaic AI Vector Search Endpoint to create.
        :param pulumi.Input[int] num_indexes: Number of indexes on the endpoint.
        """
        if creation_timestamp is not None:
            pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if creator is not None:
            pulumi.set(__self__, "creator", creator)
        if endpoint_id is not None:
            pulumi.set(__self__, "endpoint_id", endpoint_id)
        if endpoint_statuses is not None:
            pulumi.set(__self__, "endpoint_statuses", endpoint_statuses)
        if endpoint_type is not None:
            pulumi.set(__self__, "endpoint_type", endpoint_type)
        if last_updated_timestamp is not None:
            pulumi.set(__self__, "last_updated_timestamp", last_updated_timestamp)
        if last_updated_user is not None:
            pulumi.set(__self__, "last_updated_user", last_updated_user)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if num_indexes is not None:
            pulumi.set(__self__, "num_indexes", num_indexes)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> Optional[pulumi.Input[int]]:
        """
        Timestamp of endpoint creation (milliseconds).
        """
        return pulumi.get(self, "creation_timestamp")

    @creation_timestamp.setter
    def creation_timestamp(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "creation_timestamp", value)

    @property
    @pulumi.getter
    def creator(self) -> Optional[pulumi.Input[str]]:
        """
        Creator of the endpoint.
        """
        return pulumi.get(self, "creator")

    @creator.setter
    def creator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creator", value)

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique internal identifier of the endpoint (UUID).
        """
        return pulumi.get(self, "endpoint_id")

    @endpoint_id.setter
    def endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_id", value)

    @property
    @pulumi.getter(name="endpointStatuses")
    def endpoint_statuses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VectorSearchEndpointEndpointStatusArgs']]]]:
        """
        Object describing the current status of the endpoint consisting of the following fields:
        """
        return pulumi.get(self, "endpoint_statuses")

    @endpoint_statuses.setter
    def endpoint_statuses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VectorSearchEndpointEndpointStatusArgs']]]]):
        pulumi.set(self, "endpoint_statuses", value)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of Mosaic AI Vector Search Endpoint.  Currently only accepting single value: `STANDARD` (See [documentation](https://docs.databricks.com/api/workspace/vectorsearchendpoints/createendpoint) for the list of currently supported values).
        """
        return pulumi.get(self, "endpoint_type")

    @endpoint_type.setter
    def endpoint_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_type", value)

    @property
    @pulumi.getter(name="lastUpdatedTimestamp")
    def last_updated_timestamp(self) -> Optional[pulumi.Input[int]]:
        """
        Timestamp of the last update to the endpoint (milliseconds).
        """
        return pulumi.get(self, "last_updated_timestamp")

    @last_updated_timestamp.setter
    def last_updated_timestamp(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "last_updated_timestamp", value)

    @property
    @pulumi.getter(name="lastUpdatedUser")
    def last_updated_user(self) -> Optional[pulumi.Input[str]]:
        """
        User who last updated the endpoint.
        """
        return pulumi.get(self, "last_updated_user")

    @last_updated_user.setter
    def last_updated_user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_updated_user", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Mosaic AI Vector Search Endpoint to create.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="numIndexes")
    def num_indexes(self) -> Optional[pulumi.Input[int]]:
        """
        Number of indexes on the endpoint.
        """
        return pulumi.get(self, "num_indexes")

    @num_indexes.setter
    def num_indexes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "num_indexes", value)


class VectorSearchEndpoint(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 endpoint_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        > This resource can only be used on a Unity Catalog-enabled workspace!

        This resource allows you to create [Mosaic AI Vector Search Endpoint](https://docs.databricks.com/en/generative-ai/vector-search.html) in Databricks.  Mosaic AI Vector Search is a serverless similarity search engine that allows you to store a vector representation of your data, including metadata, in a vector database.  The Mosaic AI Vector Search Endpoint is used to create and access vector search indexes.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_databricks as databricks

        this = databricks.VectorSearchEndpoint("this",
            name="vector-search-test",
            endpoint_type="STANDARD")
        ```

        ## Import

        The resource can be imported using the name of the Mosaic AI Vector Search Endpoint

        bash

        ```sh
        $ pulumi import databricks:index/vectorSearchEndpoint:VectorSearchEndpoint this <endpoint-name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] endpoint_type: Type of Mosaic AI Vector Search Endpoint.  Currently only accepting single value: `STANDARD` (See [documentation](https://docs.databricks.com/api/workspace/vectorsearchendpoints/createendpoint) for the list of currently supported values).
        :param pulumi.Input[str] name: Name of the Mosaic AI Vector Search Endpoint to create.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VectorSearchEndpointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        > This resource can only be used on a Unity Catalog-enabled workspace!

        This resource allows you to create [Mosaic AI Vector Search Endpoint](https://docs.databricks.com/en/generative-ai/vector-search.html) in Databricks.  Mosaic AI Vector Search is a serverless similarity search engine that allows you to store a vector representation of your data, including metadata, in a vector database.  The Mosaic AI Vector Search Endpoint is used to create and access vector search indexes.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_databricks as databricks

        this = databricks.VectorSearchEndpoint("this",
            name="vector-search-test",
            endpoint_type="STANDARD")
        ```

        ## Import

        The resource can be imported using the name of the Mosaic AI Vector Search Endpoint

        bash

        ```sh
        $ pulumi import databricks:index/vectorSearchEndpoint:VectorSearchEndpoint this <endpoint-name>
        ```

        :param str resource_name: The name of the resource.
        :param VectorSearchEndpointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VectorSearchEndpointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 endpoint_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VectorSearchEndpointArgs.__new__(VectorSearchEndpointArgs)

            if endpoint_type is None and not opts.urn:
                raise TypeError("Missing required property 'endpoint_type'")
            __props__.__dict__["endpoint_type"] = endpoint_type
            __props__.__dict__["name"] = name
            __props__.__dict__["creation_timestamp"] = None
            __props__.__dict__["creator"] = None
            __props__.__dict__["endpoint_id"] = None
            __props__.__dict__["endpoint_statuses"] = None
            __props__.__dict__["last_updated_timestamp"] = None
            __props__.__dict__["last_updated_user"] = None
            __props__.__dict__["num_indexes"] = None
        super(VectorSearchEndpoint, __self__).__init__(
            'databricks:index/vectorSearchEndpoint:VectorSearchEndpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            creation_timestamp: Optional[pulumi.Input[int]] = None,
            creator: Optional[pulumi.Input[str]] = None,
            endpoint_id: Optional[pulumi.Input[str]] = None,
            endpoint_statuses: Optional[pulumi.Input[Sequence[pulumi.Input[Union['VectorSearchEndpointEndpointStatusArgs', 'VectorSearchEndpointEndpointStatusArgsDict']]]]] = None,
            endpoint_type: Optional[pulumi.Input[str]] = None,
            last_updated_timestamp: Optional[pulumi.Input[int]] = None,
            last_updated_user: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            num_indexes: Optional[pulumi.Input[int]] = None) -> 'VectorSearchEndpoint':
        """
        Get an existing VectorSearchEndpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] creation_timestamp: Timestamp of endpoint creation (milliseconds).
        :param pulumi.Input[str] creator: Creator of the endpoint.
        :param pulumi.Input[str] endpoint_id: Unique internal identifier of the endpoint (UUID).
        :param pulumi.Input[Sequence[pulumi.Input[Union['VectorSearchEndpointEndpointStatusArgs', 'VectorSearchEndpointEndpointStatusArgsDict']]]] endpoint_statuses: Object describing the current status of the endpoint consisting of the following fields:
        :param pulumi.Input[str] endpoint_type: Type of Mosaic AI Vector Search Endpoint.  Currently only accepting single value: `STANDARD` (See [documentation](https://docs.databricks.com/api/workspace/vectorsearchendpoints/createendpoint) for the list of currently supported values).
        :param pulumi.Input[int] last_updated_timestamp: Timestamp of the last update to the endpoint (milliseconds).
        :param pulumi.Input[str] last_updated_user: User who last updated the endpoint.
        :param pulumi.Input[str] name: Name of the Mosaic AI Vector Search Endpoint to create.
        :param pulumi.Input[int] num_indexes: Number of indexes on the endpoint.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VectorSearchEndpointState.__new__(_VectorSearchEndpointState)

        __props__.__dict__["creation_timestamp"] = creation_timestamp
        __props__.__dict__["creator"] = creator
        __props__.__dict__["endpoint_id"] = endpoint_id
        __props__.__dict__["endpoint_statuses"] = endpoint_statuses
        __props__.__dict__["endpoint_type"] = endpoint_type
        __props__.__dict__["last_updated_timestamp"] = last_updated_timestamp
        __props__.__dict__["last_updated_user"] = last_updated_user
        __props__.__dict__["name"] = name
        __props__.__dict__["num_indexes"] = num_indexes
        return VectorSearchEndpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> pulumi.Output[int]:
        """
        Timestamp of endpoint creation (milliseconds).
        """
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter
    def creator(self) -> pulumi.Output[str]:
        """
        Creator of the endpoint.
        """
        return pulumi.get(self, "creator")

    @property
    @pulumi.getter(name="endpointId")
    def endpoint_id(self) -> pulumi.Output[str]:
        """
        Unique internal identifier of the endpoint (UUID).
        """
        return pulumi.get(self, "endpoint_id")

    @property
    @pulumi.getter(name="endpointStatuses")
    def endpoint_statuses(self) -> pulumi.Output[Sequence['outputs.VectorSearchEndpointEndpointStatus']]:
        """
        Object describing the current status of the endpoint consisting of the following fields:
        """
        return pulumi.get(self, "endpoint_statuses")

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> pulumi.Output[str]:
        """
        Type of Mosaic AI Vector Search Endpoint.  Currently only accepting single value: `STANDARD` (See [documentation](https://docs.databricks.com/api/workspace/vectorsearchendpoints/createendpoint) for the list of currently supported values).
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="lastUpdatedTimestamp")
    def last_updated_timestamp(self) -> pulumi.Output[int]:
        """
        Timestamp of the last update to the endpoint (milliseconds).
        """
        return pulumi.get(self, "last_updated_timestamp")

    @property
    @pulumi.getter(name="lastUpdatedUser")
    def last_updated_user(self) -> pulumi.Output[str]:
        """
        User who last updated the endpoint.
        """
        return pulumi.get(self, "last_updated_user")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the Mosaic AI Vector Search Endpoint to create.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="numIndexes")
    def num_indexes(self) -> pulumi.Output[int]:
        """
        Number of indexes on the endpoint.
        """
        return pulumi.get(self, "num_indexes")

