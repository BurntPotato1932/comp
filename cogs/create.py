from discord.ext import commands
import requests
import os
from image_process import slide
import requests
import discord
import json
import shutil


def delete_folder(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            os.remove(file_path)

        for name in dirs:
            dir_path = os.path.join(root, name)
            shutil.rmtree(dir_path)

    shutil.rmtree(path)

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

class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='create_comp', brief='create_comp {name of the comp} {number of cards}')
    @commands.has_any_role(1004278166237487174, 1004976425599766588, 1074003818980847716)
    async def create_comp(self, ctx, msg: str, rang: int, bg: str, rng= None):
        dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
        if msg == None:
            await ctx.send('Error no name specified.')
        elif msg in dirs:
            await ctx.send('Name is taken.')
        else:
            msg = str(msg).lower()
            dirr = os.getcwd()
            inp_path = f"{dirr}\in_{msg}"
            out_path = f"{dirr}\{msg}"
            data = {
                "comp": msg,
                "bg": bg,
                "total": rang
            }
            if rng == "non_rng":
                data['rng'] = False
            try: 
                await ctx.send('Starting!')
                os.mkdir(inp_path)
                os.mkdir(out_path)
                count = 1
                for i in range(int(rang)):
                    valid_input = False
                    while not valid_input:
                        try:
                            def check(message):
                                if message.author.id == 646937666251915264 and message.channel.id == ctx.channel.id:
                                    embeds = message.embeds[0].image
                                    if len(embeds) == 0:
                                        return False
                                    url = message.embeds[0].image.url
                                    download_image(count,url, inp_path)
                                    return True
                                elif message.author.id == ctx.message.author.id and message.content == 'STOP':
                                    raise LoopEscapeException
                            await self.bot.wait_for('message', check=check)
                            await ctx.send(f'Added, wating for next card.')
                            valid_input = True
                            count += 1
                        except LoopEscapeException:
                            delete_folder(inp_path)
                            delete_folder(out_path)
                            await ctx.send('Canceled.')
                            return 
                        except:
                            await ctx.send("Invalid input, please try again.")
                await ctx.send(f'Uploaded {count-1} images to .\in_{msg}')
                file_path = os.path.join(inp_path, "data.json")
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=4)
                slide(inp_path, out_path, bg)
                await ctx.send(f'Matches made.')
            except OSError as error: 
                await ctx.send(f'Check console for error.')
                print(error)

async def setup(bot):
    await bot.add_cog(Create(bot))
