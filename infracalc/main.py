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


with open(r'/home/cortiz/dev/rivetlogic/cops/aws-calc/test/c.yaml') as file:
    infra = yaml.load(file, Loader=yaml.FullLoader)
    print(infra)
    region = REGION_SHORTS[infra["region"]]
    if infra["type"].lower() == "aws":
        for service_infra in infra["services"]:
            service_type = service_infra["service"]
            if service_type not in classCache:
                klass = my_import("infracalc.aws.{}".format(camel_to_snake(service_type)))
                classCache[service_type] = klass.AmazonEC2(region)
            service_instance = classCache[service_type]
            service_instance.price_info(service_infra)
