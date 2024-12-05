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
    'GetRegisteredModelResult',
    'AwaitableGetRegisteredModelResult',
    'get_registered_model',
    'get_registered_model_output',
]

@pulumi.output_type
class GetRegisteredModelResult:
    """
    A collection of values returned by getRegisteredModel.
    """
    def __init__(__self__, full_name=None, id=None, include_aliases=None, include_browse=None, model_infos=None):
        if full_name and not isinstance(full_name, str):
            raise TypeError("Expected argument 'full_name' to be a str")
        pulumi.set(__self__, "full_name", full_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if include_aliases and not isinstance(include_aliases, bool):
            raise TypeError("Expected argument 'include_aliases' to be a bool")
        pulumi.set(__self__, "include_aliases", include_aliases)
        if include_browse and not isinstance(include_browse, bool):
            raise TypeError("Expected argument 'include_browse' to be a bool")
        pulumi.set(__self__, "include_browse", include_browse)
        if model_infos and not isinstance(model_infos, list):
            raise TypeError("Expected argument 'model_infos' to be a list")
        pulumi.set(__self__, "model_infos", model_infos)

    @property
    @pulumi.getter(name="fullName")
    def full_name(self) -> str:
        """
        The fully-qualified name of the registered model (`catalog_name.schema_name.name`).
        """
        return pulumi.get(self, "full_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="includeAliases")
    def include_aliases(self) -> Optional[bool]:
        return pulumi.get(self, "include_aliases")

    @property
    @pulumi.getter(name="includeBrowse")
    def include_browse(self) -> Optional[bool]:
        return pulumi.get(self, "include_browse")

    @property
    @pulumi.getter(name="modelInfos")
    def model_infos(self) -> Optional[Sequence['outputs.GetRegisteredModelModelInfoResult']]:
        """
        block with information about the model in Unity Catalog:
        """
        return pulumi.get(self, "model_infos")


class AwaitableGetRegisteredModelResult(GetRegisteredModelResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegisteredModelResult(
            full_name=self.full_name,
            id=self.id,
            include_aliases=self.include_aliases,
            include_browse=self.include_browse,
            model_infos=self.model_infos)


def get_registered_model(full_name: Optional[str] = None,
                         include_aliases: Optional[bool] = None,
                         include_browse: Optional[bool] = None,
                         model_infos: Optional[Sequence[Union['GetRegisteredModelModelInfoArgs', 'GetRegisteredModelModelInfoArgsDict']]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRegisteredModelResult:
    """
    > This resource can only be used with a workspace-level provider!

    This resource allows you to get information about [Model in Unity Catalog](https://docs.databricks.com/en/mlflow/models-in-uc.html) in Databricks.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_databricks as databricks

    this = databricks.get_registered_model(full_name="main.default.my_model")
    ```

    ## Related Resources

    The following resources are often used in the same context:

    * RegisteredModel resource to manage models within Unity Catalog.
    * ModelServing to serve this model on a Databricks serving endpoint.
    * MlflowExperiment to manage [MLflow experiments](https://docs.databricks.com/data/data-sources/mlflow-experiment.html) in Databricks.


    :param str full_name: The fully-qualified name of the registered model (`catalog_name.schema_name.name`).
    :param bool include_aliases: flag to specify if list of aliases should be included into output.
    :param bool include_browse: flag to specify if include registered models in the response for which the principal can only access selective metadata for.
    :param Sequence[Union['GetRegisteredModelModelInfoArgs', 'GetRegisteredModelModelInfoArgsDict']] model_infos: block with information about the model in Unity Catalog:
    """
    __args__ = dict()
    __args__['fullName'] = full_name
    __args__['includeAliases'] = include_aliases
    __args__['includeBrowse'] = include_browse
    __args__['modelInfos'] = model_infos
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('databricks:index/getRegisteredModel:getRegisteredModel', __args__, opts=opts, typ=GetRegisteredModelResult).value

    return AwaitableGetRegisteredModelResult(
        full_name=pulumi.get(__ret__, 'full_name'),
        id=pulumi.get(__ret__, 'id'),
        include_aliases=pulumi.get(__ret__, 'include_aliases'),
        include_browse=pulumi.get(__ret__, 'include_browse'),
        model_infos=pulumi.get(__ret__, 'model_infos'))
def get_registered_model_output(full_name: Optional[pulumi.Input[str]] = None,
                                include_aliases: Optional[pulumi.Input[Optional[bool]]] = None,
                                include_browse: Optional[pulumi.Input[Optional[bool]]] = None,
                                model_infos: Optional[pulumi.Input[Optional[Sequence[Union['GetRegisteredModelModelInfoArgs', 'GetRegisteredModelModelInfoArgsDict']]]]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRegisteredModelResult]:
    """
    > This resource can only be used with a workspace-level provider!

    This resource allows you to get information about [Model in Unity Catalog](https://docs.databricks.com/en/mlflow/models-in-uc.html) in Databricks.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_databricks as databricks

    this = databricks.get_registered_model(full_name="main.default.my_model")
    ```

    ## Related Resources

    The following resources are often used in the same context:

    * RegisteredModel resource to manage models within Unity Catalog.
    * ModelServing to serve this model on a Databricks serving endpoint.
    * MlflowExperiment to manage [MLflow experiments](https://docs.databricks.com/data/data-sources/mlflow-experiment.html) in Databricks.


    :param str full_name: The fully-qualified name of the registered model (`catalog_name.schema_name.name`).
    :param bool include_aliases: flag to specify if list of aliases should be included into output.
    :param bool include_browse: flag to specify if include registered models in the response for which the principal can only access selective metadata for.
    :param Sequence[Union['GetRegisteredModelModelInfoArgs', 'GetRegisteredModelModelInfoArgsDict']] model_infos: block with information about the model in Unity Catalog:
    """
    __args__ = dict()
    __args__['fullName'] = full_name
    __args__['includeAliases'] = include_aliases
    __args__['includeBrowse'] = include_browse
    __args__['modelInfos'] = model_infos
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('databricks:index/getRegisteredModel:getRegisteredModel', __args__, opts=opts, typ=GetRegisteredModelResult)
    return __ret__.apply(lambda __response__: GetRegisteredModelResult(
        full_name=pulumi.get(__response__, 'full_name'),
        id=pulumi.get(__response__, 'id'),
        include_aliases=pulumi.get(__response__, 'include_aliases'),
        include_browse=pulumi.get(__response__, 'include_browse'),
        model_infos=pulumi.get(__response__, 'model_infos')))
