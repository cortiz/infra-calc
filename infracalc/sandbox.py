import boto3
import json
import pprint

#
# from awspricing.constants import REGION_SHORTS
#
# from infracalc.aws import aws_utils
# from infracalc.aws.amazon_ec2 import AmazonEC2
#
from infracalc.aws.aws_resource import AWSResource
from infracalc.region import REGION_SHORTS

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


def service_info(service_code):
    print("Selected {} Products".format(service_code))
    print("=====================")

    response = pricing.get_products(
        ServiceCode=service_code,
        Filters=[{'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Load Balancer-Application'},
                 {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': 'US East (N. Virginia)'},


                 ],
        MaxResults=100
    )

    for price in response['PriceList']:
        pp = pprint.PrettyPrinter(indent=1, width=300)
        pp.pprint(json.loads(price))
        print()


def all():
    print("All Services")
    print("============")
    response = pricing.describe_services()
    for service in response['Services']:
        print(service['ServiceCode'] + ": " + ", ".join(service['AttributeNames']))
    print()


#all()
service_options("AmazonEC2")
#service_info("AmazonEC2")
