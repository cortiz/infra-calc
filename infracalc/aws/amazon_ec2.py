from abc import ABC

from infracalc.aws.amazon_ebs import AmazonEBS
from infracalc.aws.aws_resource import AWSResource
from infracalc.const import HOURS_IN_A_MONTH


class AmazonEC2(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonEC2, self).__init__("AmazonEC2", "Compute Instance", "OnDemand", region)

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'tenancy',
                'Value': 'Shared'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'capacitystatus',
                'Value': 'used'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'preInstalledSw',
                'Value': 'NA'
            }]

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        attrs.pop("service")
        storage_price = None
        if "storage" in attrs:
            storage = attrs.pop("storage")
            storage["amount"] = amount
            storage["name"] = "{} for {}".format("EBS Storage", name)
            storage["service"] = AmazonEBS
            storage_price = AmazonEBS(self.region).price_info(storage)
        ec2 = self.get_pricing(attrs, amount, HOURS_IN_A_MONTH, name)
        if storage_price:
            return [ec2, storage_price]
        return ec2
