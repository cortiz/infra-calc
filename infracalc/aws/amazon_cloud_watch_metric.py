from abc import ABC

from infracalc.aws.aws_resource import AWSResource
from infracalc.aws.aws_resource_ranged import AWSResourceRanged
from infracalc.const import HOURS_IN_A_MONTH


class AmazonCloudWatchMetric(AWSResourceRanged, ABC):
    def __init__(self, region):
        super(AmazonCloudWatchMetric, self).__init__("AmazonCloudWatch", "Metric", "OnDemand", region)

    def default_attributes(self):
        return []

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        attrs.pop("service")
        return self.get_pricing(attrs, amount, 1, name)
