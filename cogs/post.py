from discord.ext import commands
import discord
import os
import time

class Post(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='post', brief='Posts the matches')
    @commands.has_any_role(1004278166237487174, 1004976425599766588, 1074003818980847716)
    async def post(self, ctx, msg=None):
        count = 1
        msg = str(msg).lower()
        temp_name = msg.replace("_", " ")
        name = temp_name.title()
        await ctx.send(f'{name}!')
        image_files = sorted(os.listdir(f"./{msg}"))
        def check(message):
            if message.author.id == 804245390642642965 and message.channel.id == ctx.channel.id:
                return True
        for f in image_files:
            if f.endswith(".png"):
                valid_input = False
                while not valid_input:
                    msg_sent = await ctx.send(f"Match {count}!", file=discord.File(f'./{msg}/{f}'))
                    count += 1
                    if ctx.message.guild.id == 1004277805950980106:
                        await self.bot.wait_for('message', check=check)
                    else:
                        await msg_sent.add_reaction("1️⃣")
                        await msg_sent.add_reaction("2️⃣")
                    time. sleep(2) 
                    valid_input = True

async def setup(bot):
    await bot.add_cog(Post(bot))
