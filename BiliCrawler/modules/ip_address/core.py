from base.base_crawler import AbstractCrawler
from bilibili_api import client


def pretty_print(zone):
    formatted_output = f"""
    IP Address Information:
    -----------------------
    IP Address     : {zone['addr']}
    Country        : {zone['country']}
    Province       : {zone['province']}
    City           : {zone['city']}
    ISP            : {zone['isp']}
    Latitude       : {zone['latitude']}
    Longitude      : {zone['longitude']}
    Zone ID        : {zone['zone_id']}
    Country Code   : {zone['country_code']}
    """
    print(formatted_output)


class IpCrawler(AbstractCrawler):

    async def start(self):
        zone = await client.get_zone()
        pretty_print(zone)
