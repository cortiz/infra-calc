from infracalc.const import HOURS_IN_A_MONTH, UNIT_HOURS, ROUND_FACTOR


class PricingInfo:
    def __init__(self, description, unit, price_per_unit, amount_of_services, amount_of_units, service_name):
        self.description = description
        self.unit = unit
        self.price_per_unit = price_per_unit
        self.service_name = service_name
        self.amount_of_units = amount_of_units
        self.amount_of_services = amount_of_services
        self.total = self.__calculate_total()

    def __str__(self):
        return "{} {}  * {} {} = {}".format(self.service_name, self.description,
                                            self.amount_of_units, self.unit, self.total)

    def __calculate_total(self):
        grand_total = float(self.price_per_unit) * self.amount_of_units
        grand_total = grand_total * float(self.amount_of_services)
        return round(grand_total, ROUND_FACTOR)

