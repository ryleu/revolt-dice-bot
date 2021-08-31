import revolt
import asyncio
import aiohttp
import json
import os
import dice_extension as diceext

try:
    token = os.environ["REVOLT_BOT_TOKEN"]
    print("Found REVOLT_BOT_TOKEN in environment variables.")
except KeyError:
    with open("token.json","r") as file:
        token = json.loads(file.read())["token"]

class Client(revolt.Client):
    commands = {}
    cogs = {}
    command_prefix = "/"
    def add_command(self,keyword,callback):
        self.commands[keyword] = callback
    async def on_message(self, message: revolt.Message):
        if not message.content.startswith(self.command_prefix):
            return
        keyword,params = (message.content[1:]+" ").split(" ",1)
        if keyword in self.commands:
            await self.commands[keyword](params, message)

async def help(params, message):
    await message.channel.send("Use `/roll` to roll things.")

async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(session, token)
        client.add_command("help", help)
        client.cogs["dice"] = diceext.Dice(client)
        await client.start()

asyncio.run(main())
