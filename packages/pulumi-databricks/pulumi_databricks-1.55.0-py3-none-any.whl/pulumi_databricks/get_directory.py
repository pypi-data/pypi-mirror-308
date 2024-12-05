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
    'GetDirectoryResult',
    'AwaitableGetDirectoryResult',
    'get_directory',
    'get_directory_output',
]

@pulumi.output_type
class GetDirectoryResult:
    """
    A collection of values returned by getDirectory.
    """
    def __init__(__self__, id=None, object_id=None, path=None, workspace_path=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if object_id and not isinstance(object_id, int):
            raise TypeError("Expected argument 'object_id' to be a int")
        pulumi.set(__self__, "object_id", object_id)
        if path and not isinstance(path, str):
            raise TypeError("Expected argument 'path' to be a str")
        pulumi.set(__self__, "path", path)
        if workspace_path and not isinstance(workspace_path, str):
            raise TypeError("Expected argument 'workspace_path' to be a str")
        pulumi.set(__self__, "workspace_path", workspace_path)

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> int:
        """
        directory object ID
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter
    def path(self) -> str:
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="workspacePath")
    def workspace_path(self) -> str:
        """
        path on Workspace File System (WSFS) in form of `/Workspace` + `path`
        """
        return pulumi.get(self, "workspace_path")


class AwaitableGetDirectoryResult(GetDirectoryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDirectoryResult(
            id=self.id,
            object_id=self.object_id,
            path=self.path,
            workspace_path=self.workspace_path)


def get_directory(id: Optional[str] = None,
                  object_id: Optional[int] = None,
                  path: Optional[str] = None,
                  workspace_path: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDirectoryResult:
    """
    > **Note** If you have a fully automated setup with workspaces created by MwsWorkspaces or azurerm_databricks_workspace, please make sure to add depends_on attribute in order to prevent _default auth: cannot configure default credentials_ errors.

    This data source allows to get information about a directory in a Databricks Workspace.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_databricks as databricks

    prod = databricks.get_directory(path="/Production")
    ```


    :param int object_id: directory object ID
    :param str path: Path to a directory in the workspace
    :param str workspace_path: path on Workspace File System (WSFS) in form of `/Workspace` + `path`
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['objectId'] = object_id
    __args__['path'] = path
    __args__['workspacePath'] = workspace_path
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('databricks:index/getDirectory:getDirectory', __args__, opts=opts, typ=GetDirectoryResult).value

    return AwaitableGetDirectoryResult(
        id=pulumi.get(__ret__, 'id'),
        object_id=pulumi.get(__ret__, 'object_id'),
        path=pulumi.get(__ret__, 'path'),
        workspace_path=pulumi.get(__ret__, 'workspace_path'))
def get_directory_output(id: Optional[pulumi.Input[Optional[str]]] = None,
                         object_id: Optional[pulumi.Input[Optional[int]]] = None,
                         path: Optional[pulumi.Input[str]] = None,
                         workspace_path: Optional[pulumi.Input[Optional[str]]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDirectoryResult]:
    """
    > **Note** If you have a fully automated setup with workspaces created by MwsWorkspaces or azurerm_databricks_workspace, please make sure to add depends_on attribute in order to prevent _default auth: cannot configure default credentials_ errors.

    This data source allows to get information about a directory in a Databricks Workspace.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_databricks as databricks

    prod = databricks.get_directory(path="/Production")
    ```


    :param int object_id: directory object ID
    :param str path: Path to a directory in the workspace
    :param str workspace_path: path on Workspace File System (WSFS) in form of `/Workspace` + `path`
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['objectId'] = object_id
    __args__['path'] = path
    __args__['workspacePath'] = workspace_path
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('databricks:index/getDirectory:getDirectory', __args__, opts=opts, typ=GetDirectoryResult)
    return __ret__.apply(lambda __response__: GetDirectoryResult(
        id=pulumi.get(__response__, 'id'),
        object_id=pulumi.get(__response__, 'object_id'),
        path=pulumi.get(__response__, 'path'),
        workspace_path=pulumi.get(__response__, 'workspace_path')))
