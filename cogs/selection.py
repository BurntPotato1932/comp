from discord.ext import commands
import requests
import discord
import os
import time
from image_process import slide
import requests
import shutil


def download_image(count, url, folder_path):
    response = requests.get(url)
    file_name = str(count)+'.png'
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "wb") as f:
        f.write(response.content)
        f.close()
    return file_name

class LoopEscapeException(Exception):
    pass

class Select_menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='1', style=discord.ButtonStyle.blurple)
    async def one(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 1
        await interaction.response.send_message('Selected 1.', ephemeral=True)
        self.stop()

    @discord.ui.button(label='2', style=discord.ButtonStyle.blurple)
    async def two(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 2
        await interaction.response.send_message('Selected 2.', ephemeral=True)
        self.stop()

    @discord.ui.button(label='X', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = 0
        await interaction.response.defer()
        self.stop()

class Select(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='select', brief='select {name of the comp} Select which card lost.')
    async def select(self, ctx, msg=None):
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
            image_files = sorted(os.listdir(inp_path))
            image_files = [f for f in image_files if f.endswith(".jpg") or f.endswith(".png")]
            other_file = sorted(os.listdir(f"./{msg}"))
            total_images = len(image_files)
            delete_list = []
            try:
                count = 0
                for f in other_file:
                    pics = f[:-4]
                    pics = pics.split("_")[1]
                    split_parts = pics.split("-")
                    image1 = split_parts[0]
                    image2 = split_parts[1]
                    view = Select_menu()
                    msg_sent = await ctx.send(f"Select who **LOST**!", file=discord.File(f'./{msg}/{f}'), view=view)
                    await view.wait()
                    if view.value is None:
                        await ctx.send("Selection timed out.")
                        raise LoopEscapeException
                    elif view.value == 1:
                        delete_list.append(os.path.join(inp_path, image1+'.png'))
                    elif view.value == 2:
                        delete_list.append(os.path.join(inp_path, image2+'.png'))
                    elif view.value == 0:
                        await ctx.send("Selection canceled.")
                        raise LoopEscapeException
                    count += 1
                for image in delete_list:
                    os.remove(image)
                await ctx.send(f'Selection complete.')
                for filename in os.listdir(out_path):
                    file_path = os.path.join(out_path, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                slide(inp_path, out_path)
                await ctx.send(f'Matches made')
            except OSError as error: 
                print(error)
            except LoopEscapeException:
                return 
            
async def setup(bot):
    await bot.add_cog(Select(bot))