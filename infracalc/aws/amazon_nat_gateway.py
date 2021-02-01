from abc import ABC

from infracalc.aws.amazon_nat_gateway_trafic import AmazonNatGatewayTraffic
from infracalc.aws.aws_resource import AWSResource
from infracalc.const import HOURS_IN_A_MONTH


class AmazonNatGateway(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonNatGateway, self).__init__("AmazonEC2", "NAT Gateway", "OnDemand", region)

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'usagetype',
                'Value': "NatGateway-Hours"
            }
        ]

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        traffic = attrs.pop("trafficPerMonth")
        attrs.pop("service")
        nat = self.get_pricing(attrs, amount, HOURS_IN_A_MONTH, name)
        traffic_name = "{} traffic per month".format(name)
        traffic_price = AmazonNatGatewayTraffic(self.region).price_info({"name": traffic_name,
                                                                         "traffic": traffic})
        return [nat, traffic_price]
