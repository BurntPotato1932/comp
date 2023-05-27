from discord.ext import commands
import requests
import os
from image_process import slide
import requests
import discord
import json
import shutil
from PIL import Image
import time

def combine_images(image1_path, image2_path, output_folder, count):
    image1 = Image.open(image1_path).convert("RGBA")
    image2 = Image.open(image2_path).convert("RGBA")

    c_size = (274, 405)
    new_image1 = image1.resize(c_size)
    new_image2 = image2.resize(c_size)
    width = new_image1.width + new_image2.width
    height = max(new_image1.height, new_image2.height)

    combined_image = Image.new("RGBA", (width, height))
    combined_image.paste(new_image1, (0, 0))

    combined_image.paste(new_image2, (new_image1.width, 0))
    combined_image_path = os.path.join(output_folder, f"{count}.png")
    combined_image.save(combined_image_path)

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
    return file_path

class LoopEscapeException(Exception):
    pass

class cr2v2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='create_2v2', brief='create_comp {name of the comp} {number of cards}')
    @commands.has_any_role(1004278166237487174, 1004976425599766588, 1074003818980847716)
    async def create_2v2(self, ctx, msg: str, rang: int, bg: str, rng= None):
        dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
        if msg == None:
            await ctx.send('Error no name specified.')
        elif msg in dirs:
            await ctx.send('Name is taken.')
        else:
            image_paths = []
            msg = str(msg).lower()
            dirr = os.getcwd()
            com_path = f"{dirr}\com_{msg}"
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
                data['2v2'] = True
                await ctx.send('Starting!')
                os.mkdir(com_path)
                os.mkdir(inp_path)
                os.mkdir(out_path)
                count = 0
                i_count = 1
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
                                    image_path = download_image(count,url, com_path)
                                    print(image_path)
                                    image_paths.append(f"com_{msg}\\{count}.png")
                                    return True
                                elif message.author.id == ctx.message.author.id and message.content == 'STOP':
                                    raise LoopEscapeException
                            await self.bot.wait_for('message', check=check)
                            await ctx.send(f'Added, wating for next card.')
                            time.sleep(2) 
                            count += 1
                            if count % 2 == 0:
                                print(count)
                                image_path1 = image_paths[0]
                                image_path2 = image_paths[1]
                                combine_images(image_path1, image_path2, inp_path, i_count)
                                image_paths = []
                                i_count += 1
                            valid_input = True
                        except LoopEscapeException:
                            delete_folder(com_path)
                            delete_folder(inp_path)
                            delete_folder(out_path)
                            await ctx.send('Canceled.')
                            return 
                        except Exception as e:
                            print(e)
                            await ctx.send("Invalid input, please try again.")
                await ctx.send(f'Uploaded {count} images to .\com_{msg}')
                time.sleep(2)
                file_path = os.path.join(inp_path, "data.json")
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=4)
                slide(inp_path, out_path, bg)
                await ctx.send(f'Matches made.')
            except OSError as error: 
                await ctx.send(f'Check console for error.')
                print(error)

async def setup(bot):
    await bot.add_cog(cr2v2(bot))
