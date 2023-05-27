from discord.ext import commands
import requests
import discord
import os
import time
from image_process import slide
import requests
import shutil
import json

class LoopEscapeException(Exception):
    pass

class Shuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='shuffle', brief='reshuffle {name of the comp}')
    @commands.has_any_role(1004278166237487174, 1004976425599766588, 1074003818980847716)
    async def reshuffle(self, ctx, msg=None):
        dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
        if msg == None:
            await ctx.send('Error no name specified.')
        elif msg not in dirs:
            await ctx.send('Name is not used.')
        else:
            msg = str(msg).lower()
            dirr = os.getcwd()
            inp_path = f"{dirr}\in_{msg}"
            out_path = f"{dirr}\{msg}"
            for filename in os.listdir(out_path):
                file_path = os.path.join(out_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            await ctx.send(f'Previous matches deleted.')
            json_file_path = os.path.join(inp_path, "data.json")
            with open(json_file_path, "r") as f:
                data = json.load(f)
            slide(inp_path, out_path, data["bg"])
            await ctx.send(f'New matches made.')


async def setup(bot):
    await bot.add_cog(Shuffle(bot))
