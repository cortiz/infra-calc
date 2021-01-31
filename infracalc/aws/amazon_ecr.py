from abc import ABC

from infracalc.aws.aws_resource import AWSResource


class AmazonECR(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonECR, self).__init__("AmazonECR", "EC2 Container Registry", "OnDemand", region)

    def default_attributes(self):
        return []

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        size = attrs.pop("size")
        attrs.pop("service")
        return self.get_pricing({}, amount, size, name)
