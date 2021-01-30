import json
from abc import ABC

from infracalc.aws.aws_resource import AWSResource
from infracalc.const import HOURS_IN_A_MONTH


class AmazonEC2(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonEC2, self).__init__("AmazonEC2", "Compute Instance", "OnDemand")
        self.region = region

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'tenancy',
                'Value': 'Shared'
            }, {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': self.product_family
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': self.region
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
        return self.get_pricing(attrs, amount, HOURS_IN_A_MONTH, name)
