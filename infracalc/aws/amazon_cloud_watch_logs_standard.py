from abc import ABC

from infracalc.aws.aws_resource import AWSResource
from infracalc.aws.aws_resource_ranged import AWSResourceRanged
from infracalc.const import HOURS_IN_A_MONTH

COMPRESSION_RATIO = 0.15  # 15%


class AmazonCloudWatchLogsRetention(AWSResource, ABC):

    def __init__(self, region):
        super(AmazonCloudWatchLogsRetention, self).__init__("AmazonCloudWatch", "Storage Snapshot", "OnDemand", region)

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'usagetype',
                'Value': 'TimedStorage-ByteHrs'
            }
        ]

    def price_info(self, attrs):
        name = attrs.pop("name")
        log_size = attrs.pop("log_size")

        return self.get_pricing(attrs, COMPRESSION_RATIO * log_size, 1, name)


class AmazonCloudWatchLogsStandard(AWSResource, ABC):
    def __init__(self, region):
        super(AmazonCloudWatchLogsStandard, self).__init__("AmazonCloudWatch", "Data Payload", "OnDemand", region)

    def default_attributes(self):
        return [
            {
                'Type': 'TERM_MATCH',
                'Field': 'usagetype',
                'Value': 'DataProcessing-Bytes'
            }
        ]

    def price_info(self, attrs):
        name = attrs.pop("name")
        amount = attrs.pop("amount")
        log_retention = 0.0
        if "logRetention" in attrs:
            log_retention = attrs.pop("logRetention")

        attrs.pop("service")
        ingestion = self.get_pricing(attrs, amount, 1, name)
        storage = AmazonCloudWatchLogsRetention(self.region).price_info({"name": "Cloudwatch retention 1 month",
                                                                          "log_size": amount})
        return [ingestion, storage]
