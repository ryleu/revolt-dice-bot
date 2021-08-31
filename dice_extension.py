import revolt
import d20

class Dice():
    def __init__(self,client):
        client.add_command("roll",self.roll)
    async def roll(self, params, message):
        try:
            result = d20.roll(params)
        except d20.errors.TooManyRolls:
            return await message.channel.send("You can't roll more than 1000 total dice.")
        except d20.errors.RollSyntaxError as err:
            return await message.channel.send(f"""{str(err)}\n```\n{params}\n{(err.col-1)*" "+len(err.got)*"^"}\n```""")
        except Exception as err:
            return await message.channel.send(f"Failed with this error:\n{str(err)}")

        #make sure the result isn't too long
        if len(str(result)) > 500:
            result = f"{params} = `{result.total}`"
        await message.channel.send(str(result))
