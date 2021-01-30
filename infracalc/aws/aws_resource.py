from abc import ABC, abstractmethod

import boto3
import json

from infracalc.price_info import PricingInfo


class AWSResource(ABC):
    def __init__(self, service_name, product_family, term_type):
        self.service_name = service_name
        self.product_family = product_family
        self.client = boto3.client('pricing')
        self.term_type = term_type

    @abstractmethod
    def default_attributes(self):
        pass

    @staticmethod
    def prepare_filters(attrs):
        filters = []
        for k in attrs:
            filters.append({'Type': 'TERM_MATCH', "Field": k, "Value": attrs[k]})
        return filters

    def __get_service_info(self, attrs):
        response = self.client.get_products(
            ServiceCode=self.service_name,
            Filters=self.default_attributes() + self.prepare_filters(attrs),
            MaxResults=1
        )
        return response

    @staticmethod
    def __get_service_pricing(price):

        for k in price.keys():
            data_key = next(iter(price[k]['priceDimensions'].keys()))
            pricing_data = price[k]['priceDimensions'][data_key]
            return {"desc": pricing_data["description"], "unit": pricing_data["unit"],
                    "pricePerUnit": pricing_data["pricePerUnit"]["USD"]}

    def get_pricing(self, attrs, amount_of_services, amount_of_units, service_name):
        response = self.__get_service_info(attrs)
        raw = self.__get_service_pricing(json.loads(response['PriceList'][0])['terms'][self.term_type])
        return PricingInfo(raw["desc"], raw["unit"], raw["pricePerUnit"], amount_of_services, amount_of_units,
                           service_name)
