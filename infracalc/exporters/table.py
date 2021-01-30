from colorclass import Color
from terminaltables import AsciiTable

from infracalc.const import ROUND_FACTOR
from infracalc.exporters.exporter import Exporter


class Table(Exporter):

    def __init__(self, pricing_information, attrs):
        super(Table, self).__init__(pricing_information, attrs)

    def export(self):
        data = [
            ["Name", "Service description", "Unit", "Price per unit", "Amount of units", "Amount of services", "Total"]
        ]
        final_total = 0.0
        for service in self.pricing_information:
            data.append([
                service.service_name,
                service.description,
                service.unit,
                service.price_per_unit,
                service.amount_of_units,
                service.amount_of_services,
                Color('{autogreen}' + str(service.total) + '{/autogreen}')
            ])
            final_total += service.total
        table = AsciiTable(data)
        print(table.table)
        print()
        print("Total:\r")
        print(Color('\t{autogreen}' + str(round(final_total, ROUND_FACTOR)) + '{/autogreen}'))
