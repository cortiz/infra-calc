import json
from abc import ABC, abstractmethod

import boto3

from infracalc.price_info import PricingInfo


class AWSResource(ABC):
    def __init__(self, service_name, product_family, term_type, region):
        self.service_name = service_name
        self.product_family = product_family
        self.client = boto3.client('pricing')
        self.term_type = term_type
        self.region = region

    @abstractmethod
    def default_attributes(self):
        pass

    def _base_attrs(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': self.product_family
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': self.region
            }
        ]

    @staticmethod
    def prepare_filters(attrs):
        filters = []
        for k in attrs:
            filters.append({'Type': 'TERM_MATCH', "Field": k, "Value": attrs[k]})
        return filters

    def _get_service_info(self, attrs):
        response = self.client.get_products(
            ServiceCode=self.service_name,
            Filters=self._base_attrs() + self.default_attributes() + self.prepare_filters(attrs),
            MaxResults=1
        )
        return response

    def _get_service_pricing(self, price):

        for k in price.keys():
            data_key = next(iter(price[k]['priceDimensions'].keys()))
            pricing_data = price[k]['priceDimensions'][data_key]
            return {"desc": pricing_data["description"], "unit": pricing_data["unit"],
                    "pricePerUnit": pricing_data["pricePerUnit"]["USD"]}

    def get_pricing(self, attrs, amount_of_services, amount_of_units, service_name):
        response = self._get_service_info(attrs)
        raw = self._get_service_pricing(json.loads(response['PriceList'][0])['terms'][self.term_type])
        return PricingInfo(raw["desc"], raw["unit"], raw["pricePerUnit"], amount_of_services, amount_of_units,
                           service_name)
