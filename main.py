import discord
from discord.ext import commands
import asyncio
import datetime
import os
from dotenv import load_dotenv
from os import getenv
load_dotenv()

cogs = [
   "comp_commands.selection",
   "comp_commands.background",
   "comp_commands.post",
   "comp_commands.create",
   "comp_commands.reshuffle",
   "comp_commands.2v2_create",
   "comp_commands.svs_create"
]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=';', intents=intents)

@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}\nDiscord.py Version: {discord.__version__}  Date: {datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S %p")}\n')

@bot.command()
async def pong(ctx):
  await ctx.reply('aaa')

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please add all Arguments.')
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You lack the required permissions for this command.")
  if isinstance(error, commands.NSFWChannelRequired):
    await ctx.send("This command can only be run in a NSFW channel.")
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.send("You are using this command too fast!")

async def load():
    for f in cogs:
      print(f + (' has loaded!'))
      await bot.load_extension(f)

async def main():
  await load()
  await bot.start(getenv('TOKEN'))

asyncio.run(main())
