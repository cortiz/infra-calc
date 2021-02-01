from abc import ABC

from infracalc.aws.aws_resource import AWSResource
from infracalc.aws.aws_resource_ranged import AWSResourceRanged
from infracalc.const import HOURS_IN_A_MONTH


class AmazonS3(AWSResourceRanged, ABC):
    def __init__(self, region):
        super(AmazonS3, self).__init__("AmazonS3", "Storage", "OnDemand", region)

    def default_attributes(self):
        return []

    def price_info(self, attrs):
        name = attrs.pop("name")
        size = attrs.pop("size")
        attrs.pop("service")
        return self.get_pricing(attrs, size, 1, name)
