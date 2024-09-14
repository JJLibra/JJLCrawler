import sys
import asyncio
import cmd_arg


async def main():
    # parse cmd
    await cmd_arg.parse_cmd()

    pass


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit()
