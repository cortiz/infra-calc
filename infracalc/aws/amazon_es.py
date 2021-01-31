from abc import ABC

from infracalc.aws.amazon_es_storage import AmazonESStorage
from infracalc.aws.amazon_rds_storage import AmazonRDSStorage
from infracalc.aws.aws_resource import AWSResource
from infracalc.const import HOURS_IN_A_MONTH


class AmazonES(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonES, self).__init__("AmazonES", "Elastic Search Instance", "OnDemand", region)

    def default_attributes(self):
        return []

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        storage = attrs.pop("storage")
        storage["name"] = name
        storage["nodes"] = amount
        attrs.pop("service")
        es = self.get_pricing(attrs, amount, HOURS_IN_A_MONTH, name)
        storage = AmazonESStorage(self.region).price_info(storage)
        return [es, storage]
