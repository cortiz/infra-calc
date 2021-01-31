from abc import ABC

from infracalc.aws.aws_resource import AWSResource


class AmazonRDSStorage(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonRDSStorage, self).__init__("AmazonRDS", "Database Storage", "OnDemand", region)

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
        name = attrs.pop("name") + "DB Storage"
        return self.get_pricing(attrs, 1, size, name)
