from abc import ABC

from infracalc.aws.aws_resource import AWSResource


class AmazonEBS(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonEBS, self).__init__("AmazonEC2", "Storage", "OnDemand", region)

    def default_attributes(self):
        return []

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        size = attrs.pop("size")
        attrs.pop("service")
        return self.get_pricing(attrs, amount, size, name)
