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
    'GetAwsCrossAccountPolicyResult',
    'AwaitableGetAwsCrossAccountPolicyResult',
    'get_aws_cross_account_policy',
    'get_aws_cross_account_policy_output',
]

@pulumi.output_type
class GetAwsCrossAccountPolicyResult:
    """
    A collection of values returned by getAwsCrossAccountPolicy.
    """
    def __init__(__self__, aws_account_id=None, id=None, json=None, pass_roles=None, policy_type=None, region=None, security_group_id=None, vpc_id=None):
        if aws_account_id and not isinstance(aws_account_id, str):
            raise TypeError("Expected argument 'aws_account_id' to be a str")
        pulumi.set(__self__, "aws_account_id", aws_account_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if json and not isinstance(json, str):
            raise TypeError("Expected argument 'json' to be a str")
        pulumi.set(__self__, "json", json)
        if pass_roles and not isinstance(pass_roles, list):
            raise TypeError("Expected argument 'pass_roles' to be a list")
        pulumi.set(__self__, "pass_roles", pass_roles)
        if policy_type and not isinstance(policy_type, str):
            raise TypeError("Expected argument 'policy_type' to be a str")
        pulumi.set(__self__, "policy_type", policy_type)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if security_group_id and not isinstance(security_group_id, str):
            raise TypeError("Expected argument 'security_group_id' to be a str")
        pulumi.set(__self__, "security_group_id", security_group_id)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> Optional[str]:
        return pulumi.get(self, "aws_account_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def json(self) -> str:
        """
        AWS IAM Policy JSON document
        """
        return pulumi.get(self, "json")

    @property
    @pulumi.getter(name="passRoles")
    def pass_roles(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "pass_roles")

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> Optional[str]:
        return pulumi.get(self, "policy_type")

    @property
    @pulumi.getter
    def region(self) -> Optional[str]:
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="securityGroupId")
    def security_group_id(self) -> Optional[str]:
        return pulumi.get(self, "security_group_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        return pulumi.get(self, "vpc_id")


class AwaitableGetAwsCrossAccountPolicyResult(GetAwsCrossAccountPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAwsCrossAccountPolicyResult(
            aws_account_id=self.aws_account_id,
            id=self.id,
            json=self.json,
            pass_roles=self.pass_roles,
            policy_type=self.policy_type,
            region=self.region,
            security_group_id=self.security_group_id,
            vpc_id=self.vpc_id)


def get_aws_cross_account_policy(aws_account_id: Optional[str] = None,
                                 pass_roles: Optional[Sequence[str]] = None,
                                 policy_type: Optional[str] = None,
                                 region: Optional[str] = None,
                                 security_group_id: Optional[str] = None,
                                 vpc_id: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAwsCrossAccountPolicyResult:
    """
    > **Note** This data source can only be used with an account-level provider!

    This data source constructs necessary AWS cross-account policy for you, which is based on [official documentation](https://docs.databricks.com/administration-guide/account-api/iam-role.html#language-Your%C2%A0VPC,%C2%A0default).

    ## Example Usage

    For more detailed usage please see get_aws_assume_role_policy or databricks_aws_s3_mount pages.

    ```python
    import pulumi
    import pulumi_databricks as databricks

    this = databricks.get_aws_cross_account_policy()
    ```

    ## Related Resources

    The following resources are used in the same context:

    * Provisioning AWS Databricks workspaces with a Hub & Spoke firewall for data exfiltration protection guide
    * get_aws_assume_role_policy data to construct the necessary AWS STS assume role policy.
    * get_aws_bucket_policy data to configure a simple access policy for AWS S3 buckets, so that Databricks can access data in it.
    * InstanceProfile to manage AWS EC2 instance profiles that users can launch Cluster and access data, like databricks_mount.


    :param str aws_account_id: — Your AWS account ID, which is a number.
    :param Sequence[str] pass_roles: List of Data IAM role ARNs that are explicitly granted `iam:PassRole` action.
           The below arguments are only valid for `restricted` policy type
    :param str policy_type: The type of cross account policy to generated: `managed` for Databricks-managed VPC and `customer` for customer-managed VPC, `restricted` for customer-managed VPC with policy restrictions
    :param str region: — AWS Region name for your VPC deployment, for example `us-west-2`.
    :param str security_group_id: — ID of your AWS security group. When you add a security group restriction, you cannot reuse the cross-account IAM role or reference a credentials ID (`credentials_id`) for any other workspaces. For those other workspaces, you must create separate roles, policies, and credentials objects.
    :param str vpc_id: — ID of the AWS VPC where you want to launch workspaces.
    """
    __args__ = dict()
    __args__['awsAccountId'] = aws_account_id
    __args__['passRoles'] = pass_roles
    __args__['policyType'] = policy_type
    __args__['region'] = region
    __args__['securityGroupId'] = security_group_id
    __args__['vpcId'] = vpc_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('databricks:index/getAwsCrossAccountPolicy:getAwsCrossAccountPolicy', __args__, opts=opts, typ=GetAwsCrossAccountPolicyResult).value

    return AwaitableGetAwsCrossAccountPolicyResult(
        aws_account_id=pulumi.get(__ret__, 'aws_account_id'),
        id=pulumi.get(__ret__, 'id'),
        json=pulumi.get(__ret__, 'json'),
        pass_roles=pulumi.get(__ret__, 'pass_roles'),
        policy_type=pulumi.get(__ret__, 'policy_type'),
        region=pulumi.get(__ret__, 'region'),
        security_group_id=pulumi.get(__ret__, 'security_group_id'),
        vpc_id=pulumi.get(__ret__, 'vpc_id'))
def get_aws_cross_account_policy_output(aws_account_id: Optional[pulumi.Input[Optional[str]]] = None,
                                        pass_roles: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                        policy_type: Optional[pulumi.Input[Optional[str]]] = None,
                                        region: Optional[pulumi.Input[Optional[str]]] = None,
                                        security_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                                        vpc_id: Optional[pulumi.Input[Optional[str]]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAwsCrossAccountPolicyResult]:
    """
    > **Note** This data source can only be used with an account-level provider!

    This data source constructs necessary AWS cross-account policy for you, which is based on [official documentation](https://docs.databricks.com/administration-guide/account-api/iam-role.html#language-Your%C2%A0VPC,%C2%A0default).

    ## Example Usage

    For more detailed usage please see get_aws_assume_role_policy or databricks_aws_s3_mount pages.

    ```python
    import pulumi
    import pulumi_databricks as databricks

    this = databricks.get_aws_cross_account_policy()
    ```

    ## Related Resources

    The following resources are used in the same context:

    * Provisioning AWS Databricks workspaces with a Hub & Spoke firewall for data exfiltration protection guide
    * get_aws_assume_role_policy data to construct the necessary AWS STS assume role policy.
    * get_aws_bucket_policy data to configure a simple access policy for AWS S3 buckets, so that Databricks can access data in it.
    * InstanceProfile to manage AWS EC2 instance profiles that users can launch Cluster and access data, like databricks_mount.


    :param str aws_account_id: — Your AWS account ID, which is a number.
    :param Sequence[str] pass_roles: List of Data IAM role ARNs that are explicitly granted `iam:PassRole` action.
           The below arguments are only valid for `restricted` policy type
    :param str policy_type: The type of cross account policy to generated: `managed` for Databricks-managed VPC and `customer` for customer-managed VPC, `restricted` for customer-managed VPC with policy restrictions
    :param str region: — AWS Region name for your VPC deployment, for example `us-west-2`.
    :param str security_group_id: — ID of your AWS security group. When you add a security group restriction, you cannot reuse the cross-account IAM role or reference a credentials ID (`credentials_id`) for any other workspaces. For those other workspaces, you must create separate roles, policies, and credentials objects.
    :param str vpc_id: — ID of the AWS VPC where you want to launch workspaces.
    """
    __args__ = dict()
    __args__['awsAccountId'] = aws_account_id
    __args__['passRoles'] = pass_roles
    __args__['policyType'] = policy_type
    __args__['region'] = region
    __args__['securityGroupId'] = security_group_id
    __args__['vpcId'] = vpc_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('databricks:index/getAwsCrossAccountPolicy:getAwsCrossAccountPolicy', __args__, opts=opts, typ=GetAwsCrossAccountPolicyResult)
    return __ret__.apply(lambda __response__: GetAwsCrossAccountPolicyResult(
        aws_account_id=pulumi.get(__response__, 'aws_account_id'),
        id=pulumi.get(__response__, 'id'),
        json=pulumi.get(__response__, 'json'),
        pass_roles=pulumi.get(__response__, 'pass_roles'),
        policy_type=pulumi.get(__response__, 'policy_type'),
        region=pulumi.get(__response__, 'region'),
        security_group_id=pulumi.get(__response__, 'security_group_id'),
        vpc_id=pulumi.get(__response__, 'vpc_id')))
