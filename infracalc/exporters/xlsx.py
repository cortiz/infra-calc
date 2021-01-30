from pathlib import Path
from sys import path

import xlsxwriter

from infracalc.exporters.exporter import Exporter


class Xlsx(Exporter):
    def __init__(self, services, attrs):
        super(Xlsx, self).__init__(services, attrs)

    def export(self):
        self.__create_workbook(self.attrs["file"])

    def __create_workbook(self, file):
        workbook = xlsxwriter.Workbook(file)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        money = workbook.add_format({'num_format': '$###,###.##0'})
        bold_money = workbook.add_format({'num_format': '$###,###.##0', 'bold': True})

        worksheet.write('B2', 'Name', bold)
        worksheet.write('C2', 'Service description', bold)
        worksheet.write('D2', 'Unit', bold)
        worksheet.write('E2', 'Price per unit', bold)
        worksheet.write('F2', 'Amount of units', bold)
        worksheet.write('G2', 'Amount of services', bold)
        worksheet.write('H2', 'Total', bold)
        row = 2
        col = 1
        sum_total = 0.0
        for service in self.pricing_information:
            worksheet.write(row, col, service.service_name)
            worksheet.write(row, col + 1, service.description)
            worksheet.write(row, col + 2, service.unit)
            worksheet.write(row, col + 3, service.price_per_unit, money)
            worksheet.write(row, col + 4, service.amount_of_units)
            worksheet.write(row, col + 5, service.amount_of_services)
            worksheet.write(row, col + 6, service.total, money)
            sum_total += service.total
            row += 1
        worksheet.write(row + 1, col + 5, "Total per Month", bold)
        worksheet.write(row + 1, col + 6, sum_total, bold_money)
        workbook.close()
