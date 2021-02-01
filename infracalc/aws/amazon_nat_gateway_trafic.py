from abc import ABC

from infracalc.aws.aws_resource import AWSResource
from infracalc.const import HOURS_IN_A_MONTH


class AmazonNatGatewayTraffic(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonNatGatewayTraffic, self).__init__("AmazonEC2", "NAT Gateway", "OnDemand", region)

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'usagetype',
                'Value': "NatGateway-Bytes"
            }
        ]

    def price_info(self, attrs):
        name = attrs.pop("name")
        traffic = attrs.pop("traffic")
        return self.get_pricing({}, traffic, 1, name)
