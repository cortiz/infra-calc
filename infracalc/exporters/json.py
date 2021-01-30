import json
from infracalc.const import ROUND_FACTOR

from infracalc.exporters.exporter import Exporter


class JSON(Exporter):

    def __init__(self, pricing_information, attrs):
        super(JSON, self).__init__(pricing_information, attrs)

    def export(self):
        result = {
            "total": {
                "total": round(sum(float(service.total) for service in self.pricing_information), ROUND_FACTOR)
            },
            "details": self.pricing_information
        }
        print(json.dumps(result, default=lambda x: x.__dict__))
