from abc import ABC

from infracalc.aws.aws_resource import AWSResource
from infracalc.const import HOURS_IN_A_MONTH


class AmazonALB(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonALB, self).__init__("AmazonEC2", "Load Balancer-Application", "OnDemand", region)

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'usagetype',
                'Value': 'LoadBalancerUsage'
            }
        ]

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        attrs.pop("service")
        return self.get_pricing({}, amount, HOURS_IN_A_MONTH, name)
