import importlib
import re

import boto3
import yaml

from region import REGION_SHORTS

client = boto3.client('pricing')
classCache = {}




pricing_info = []
with open(r'/home/cortiz/repos/infra-calc/test/c.yaml') as file:
    infra = yaml.load(file, Loader=yaml.FullLoader)
    region = REGION_SHORTS[infra["region"]]
    pricing_api = infra["type"]
    if infra["type"].lower() == "aws":
        for service_infra in infra["services"]:
            service_type = service_infra["service"]
            if service_type not in classCache:
                module = my_import("infracalc.{}.{}".format(pricing_api, camel_to_snake(service_type)))
                klass = getattr(module, service_type)
                classCache[service_type] = klass(region)
            service_instance = classCache[service_type]
            pricing_info.append(service_instance.price_info(service_infra))
    if "export" in infra:
        exporter = infra["export"]["exporter"]
        params = infra["export"]["params"]
        export_module = my_import("infracalc.{}.{}".format("exporters", camel_to_snake(exporter)))
        exporter_klass = getattr(export_module, exporter)
        exporter_klass(pricing_info, params).export()
