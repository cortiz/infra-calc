from abc import ABC

from infracalc.aws.amazon_rds_storage import AmazonRDSStorage
from infracalc.aws.aws_resource import AWSResource
from infracalc.const import HOURS_IN_A_MONTH


class AmazonRDS(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonRDS, self).__init__("AmazonRDS", "Database Instance", "OnDemand", region)

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'termType',
                'Value': self.term_type
            }
        ]

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        storage = attrs.pop("storage")
        storage["name"] = name
        attrs.pop("service")
        db = self.get_pricing(attrs, amount, HOURS_IN_A_MONTH, name)
        storage = AmazonRDSStorage(self.region).price_info(storage)
        return [db, storage]
