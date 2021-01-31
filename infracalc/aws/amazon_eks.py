from abc import ABC

from infracalc.aws.aws_resource import AWSResource
from infracalc.const import HOURS_IN_A_MONTH


class AmazonEKS(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonEKS, self).__init__("AmazonEKS", "Compute", "OnDemand", region)

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'tiertype',
                'Value': "HAStandard"
            }
        ]

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        attrs.pop("service")
        return self.get_pricing(attrs, amount, HOURS_IN_A_MONTH, name)
