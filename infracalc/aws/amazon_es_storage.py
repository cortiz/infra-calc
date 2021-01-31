from abc import ABC

from infracalc.aws.aws_resource import AWSResource


class AmazonESStorage(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonESStorage, self).__init__("AmazonES", "Elastic Search Volume", "OnDemand", region)

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'termType',
                'Value': self.term_type
            }
        ]

    def price_info(self, attrs):
        size = attrs.pop("size")
        name = attrs.pop("name") + "ES Storage"
        nodes = attrs.pop("nodes")
        return self.get_pricing(attrs, nodes, size, name)
