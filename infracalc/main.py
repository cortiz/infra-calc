import boto3
import json
import yaml
from region import REGION_SHORTS
import re
import importlib

client = boto3.client('pricing')
classCache = {}


def my_import(name):
    print(name)
    cls = importlib.import_module(name)
    return cls


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


with open(r'../test/c.yaml') as file:
    infra = yaml.load(file, Loader=yaml.FullLoader)
    print(infra)
    region = REGION_SHORTS[infra["region"]]
    if infra["type"].lower() == "aws":
        for s in infra["services"].keys():
            if not s in classCache:
                klass = my_import("infracalc.aws.{}".format(camel_to_snake(s)))
                classCache[s] = klass.Calculator(client, region)
            service = service = classCache[s]
            print(service.total(infra["services"][s]))

#
# r = client.get_products(
#     ServiceCode='amazon_ec2.py',
#     Filters=[
#         {
#             'Type': 'TERM_MATCH',
#             'Field': 'productFamily',
#             'Value': 'Storage'
#         },
#         {
#             'Type': 'TERM_MATCH',
#             'Field': 'location',
#             'Value': 'US East (N. Virginia)'
#         },
#         {
#             'Type': 'TERM_MATCH',
#             'Field': 'volumeApiName',
#             'Value': 'gp3'
#         },
#
#     ]
# )
#
# price_list2 = r["PriceList"]
# for s in price_list2:
#     price_item = json.loads(s)
#     terms = price_item["terms"]["OnDemand"]
#     key = list(terms.keys())[0]
#     key2 = list(terms[key]["priceDimensions"])[0]
#     priceInfo = terms[key]["priceDimensions"][key2]
#     price = float(priceInfo["pricePerUnit"]["USD"]) * 30
#     print(round(price, 6))
#
