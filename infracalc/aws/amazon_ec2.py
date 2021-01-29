import json


class Calculator:
    def __init__(self, client, region):
        self.client = client
        self.region = region

    def total(self, attrs):
        price_per_unit = 0
        response = self.client.get_products(
            ServiceCode='AmazonEC2',
            Filters=[
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'operatingSystem',
                    'Value': attrs["operatingSystem"]
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'tenancy',
                    'Value': 'Shared'
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'instanceType',
                    'Value': attrs["type"]
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'location',
                    'Value': self.region
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'capacitystatus',
                    'Value': 'used'
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'preInstalledSw',
                    'Value': 'NA'
                }
            ]
        )
        price_list = response["PriceList"]
        for s in price_list:
            price_item = json.loads(s)
            terms = price_item["terms"]["OnDemand"]
            key = list(terms.keys())[0]
            key2 = list(terms[key]["priceDimensions"])[0]
            price_info = terms[key]["priceDimensions"][key2]
            price = float(price_info["pricePerUnit"]["USD"]) * 730  # Hardcoded for now (hours in a month)
            price_per_unit = round(price, 6)
            break

        return round(price_per_unit + self.total_disk(attrs["disk"]), 6)

    def total_disk(self, disk):
        r = self.client.get_products(
            ServiceCode='AmazonEC2',
            Filters=[
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'productFamily',
                    'Value': 'Storage'
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'location',
                    'Value': self.region
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'volumeApiName',
                    'Value': disk["type"]
                },
            ]
        )
        price_list2 = r["PriceList"]
        for s in price_list2:
            price_item = json.loads(s)
            terms = price_item["terms"]["OnDemand"]
            key = list(terms.keys())[0]
            key2 = list(terms[key]["priceDimensions"])[0]
            priceInfo = terms[key]["priceDimensions"][key2]
            price = float(priceInfo["pricePerUnit"]["USD"]) * disk["size"]

            return round(price, 6)
