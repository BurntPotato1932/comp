from discord.ext import commands
import requests
import os
import discord
import os
import json
from PIL import Image

def CC(card):
    x, y = map(int, card.split(","))
    return [x, y]

def download_image(name , url, folder_path):
    response = requests.get(url)
    file_name = str(name)+'.png'
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "wb") as f:
        f.write(response.content)
        f.close()
    return file_name

def save_png_details(file_path, card1, card2):
    try:
        directory = os.path.dirname(file_path)
        img = Image.open(file_path)

        details = {
            "name": str("bgs\\" + os.path.basename(img.filename)),
            "x1": CC(card1)[0],
            "y1": CC(card1)[1],
            "x2": CC(card2)[0],
            "y2": CC(card2)[1]
        }

        file_name = os.path.splitext(img.filename)[0]
        output_file = os.path.join(directory, file_name + ".json")
        with open(output_file, "w") as f:
            json.dump(details, f, indent=4)
    except Exception as e:
        print(f"Error: {e}")

class Background(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='add_bg', brief='')
    @commands.has_any_role(1004278166237487174, 1004976425599766588, 1074003818980847716)
    async def add_bg(self, ctx, name: str, card1: str, card2: str):
        dir = os.getcwd()
        path = f"{dir}\\bgs"
        img_path = f"{dir}\\bgs\\{name}.png"
        if ctx.message.attachments:
            url = ctx.message.attachments[0].url
            download_image(name, url, path)
            save_png_details(img_path, card1, card2)
            await ctx.reply(f'Saved {name}.png')



async def setup(bot):
    await bot.add_cog(Background(bot))
