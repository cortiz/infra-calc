import json
import sys
from abc import ABC, abstractmethod

import boto3

from infracalc.aws.aws_resource import AWSResource
from infracalc.price_info import PricingInfo


class AWSResourceRanged(AWSResource, ABC):

    def _get_service_pricing(self, price, amount):
        for k in price.keys():
            for pricing_data_key in price[k]['priceDimensions'].keys():
                pricing_data=price[k]['priceDimensions'][pricing_data_key]
                if pricing_data["endRange"] == "Inf":
                    pricing_data["endRange"]=sys.maxsize
                if amount in range(int(pricing_data["beginRange"]), int(pricing_data["endRange"])):
                    return {"desc": pricing_data["description"], "unit": pricing_data["unit"],
                            "pricePerUnit": pricing_data["pricePerUnit"]["USD"]}

    def get_pricing(self, attrs, amount_of_services, amount_of_units, service_name):
        response = self._get_service_info(attrs)
        raw = self._get_service_pricing(json.loads(response['PriceList'][0])['terms'][self.term_type], amount_of_services)
        return PricingInfo(raw["desc"], raw["unit"], raw["pricePerUnit"], amount_of_services, amount_of_units,
                           service_name)
