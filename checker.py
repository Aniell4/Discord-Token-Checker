import asyncio
import aiosonic
import json
from random import randint
from colorama import init, Fore, Back, Style
init(convert=True)

async def check(token, client):
    response = await client.get(f'https://discord.com/api/v9/users/@me/guild-events', headers={'Authorization': token})
    if "You need to verify your account in order to perform this action." in str(await response.text()) or "401: Unauthorized" in str(await response.text()):
        return False
    else:
        return True

async def main():
    client = aiosonic.HTTPClient()
    try:
        checked = []
        with open('tokens.txt', 'r') as tokens:
            for token in tokens.read().split('\n'):
                if len(token) > 15 and token not in checked and await check(token, client) == True:
                    print(f'{Fore.GREEN}[Valid]{Fore.WHITE} {token} ')
                    print(Style.RESET_ALL, end='')
                    checked.append(token)
                else:
                    print(f'{Fore.RED}[Invalid]{Fore.WHITE} {token}')
                    print(Style.RESET_ALL, end='')
            await client.shutdown()
        if len(checked) > 0:
            save = input(f'{len(checked)} valid tokens\nSave to File (y/n)').lower()
            if save == 'y':
                name = randint(100000000, 9999999999)
                with open(f'{name}.txt', 'w') as saveFile:
                    saveFile.write('\n'.join(checked))
                print(f'Tokens Save To {name}.txt File!')
        input('Press Enter To Exit...')
    except:
        input('Can\'t Open "tokens.txt" File!')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
