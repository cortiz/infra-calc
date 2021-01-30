import json
from abc import ABC

from infracalc.aws.aws_resource import AWSResource


class AmazonEBS(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonEBS, self).__init__("AmazonEC2", "Storage", "OnDemand")
        self.region = region

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': self.product_family
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': self.region
            }]

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        size = attrs.pop("size")
        attrs.pop("service")
        return self.get_pricing(attrs, amount, size, name)
