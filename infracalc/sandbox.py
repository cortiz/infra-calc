import boto3
import json
import pprint
#
# from awspricing.constants import REGION_SHORTS
#
# from infracalc.aws import aws_utils
# from infracalc.aws.amazon_ec2 import AmazonEC2
#
pricing = boto3.client("pricing")
#
#
def service_options(service_name):
    print("Selected EC2 Attributes & Values")
    print("================================")
    response = pricing.describe_services(ServiceCode=service_name)
    attrs = response['Services'][0]['AttributeNames']

    for attr in attrs:
        response = pricing.get_attribute_values(ServiceCode=service_name, AttributeName=attr)

        values = []
        for attr_value in response['AttributeValues']:
            values.append(attr_value['Value'])
        print("  " + attr + ": " + ", ".join(values))

#
# def print_service_info(service_name, attrs):
#     print("Selected EC2 Products")
#     print("=====================")
#
#     response = aws_utils.service_info(service_name, attrs)
#     for price in response['PriceList']:
#         pp = pprint.PrettyPrinter(indent=1, width=300)
#         price = json.loads(price)
#         pp.pprint(price)
#         print()
#
#
service_options("AmazonEC2")
#
# # print_service_info("AmazonRDS",
# #                    {'location': REGION_SHORTS["us-east-1"], 'productFamily': 'Database Storage',
# #                     'volumeType': 'General Purpose','termType': 'OnDemand','deploymentOption': 'Single-AZ'})
# #
# # data = get_prining_info("AmazonRDS",
# #                         {'location': REGION_SHORTS["us-east-1"], 'databaseEngine': 'PostgreSQL',
# #                          'instanceType': 'db.m4.10xlarge', 'deploymentOption': 'Single-AZ',
# #                          'termType': 'OnDemand'})
# # print(round(float(data["pricePerUnit"]) * 730, 6))
# #
# # disk_data = aws_utils.get_pricing(pricing, "AmazonRDS",
# #                                   {'location': REGION_SHORTS["us-east-1"], 'productFamily': 'Database Storage',
# #                                    'volumeType': 'General Purpose', 'termType': 'OnDemand',
# #                                    'deploymentOption': 'Single-AZ'})
# #
# # print(round(float(disk_data["pricePerUnit"]) * 30, 6))
#
# AmazonEC2().get_pricing([{}])
