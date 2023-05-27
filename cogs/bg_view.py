from discord.ext import commands
import discord
import os
from PIL import Image
import json

def dimensions(path):
    with Image.open(path) as img:
        return img.size

def json_file(bg):
    json_file_path = os.path.join("bgs", f"{bg}.json")
    with open(json_file_path, "r") as f:
        data = json.load(f)
        return data

class Dropdown(discord.ui.Select):
    def __init__(self):
        image_files = os.listdir("bgs")
        image_files = [f for f in image_files if f.endswith(".png")]
        options = [discord.SelectOption(label=name, value=name) for name in image_files]
        super().__init__(placeholder='Select a background.',options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        img = str(self.values[0])
        width, height = dimensions(f"bgs\\{img}")
        data = json_file(img[:-4])
        x1, y1 = data["x1"], data["y1"]
        x2, y2 = data["x2"], data["y2"]
        nf = [discord.File(f"bgs\\{img}", filename=img)]
        ne = discord.Embed(title="Background View", description=f"**{img}**: {width}x{height}\n**x1,y1**: {x1},{y1}\n**x2,y2**: {x2},{y2}")
        ne.set_image(url=f"attachment://{img}")
        await interaction.response.edit_message(attachments=nf, embed=ne)

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Dropdown())

class Bg_view(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='view_bgs')
    async def view_bgs(self, ctx):
        view = DropdownView()
        width, height = dimensions("bgs\\default.png")
        data = json_file("default")
        x1, y1 = data["x1"], data["y1"]
        x2, y2 = data["x2"], data["y2"]
        f = discord.File("bgs\\default.png", filename="default.png")
        e = discord.Embed(title="Background View", description=f"**default.png**: {width}x{height}\n**x1,y1**: {x1},{y1}\n**x2,y2**: {x2},{y2}")
        e.set_image(url="attachment://default.png")
        await ctx.send(file=f, embed=e, view=view)


async def setup(bot):
    await bot.add_cog(Bg_view(bot))
