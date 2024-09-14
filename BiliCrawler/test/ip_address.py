from bilibili_api import client, sync


async def main():
    zone = await client.get_zone()
    print(zone)

sync(main())
