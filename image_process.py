import os
from PIL import Image
import random
import json

def slide(inp, outp, bg):
    json_file_path = os.path.join("bgs", f"{bg}.json")
    with open(json_file_path, "r") as f:
        data = json.load(f)
    rn = True
    input_folder = inp
    output_folder = outp

    def process_image(image1_path, image2_path):
        bg_image = Image.open(data["name"]).convert("RGBA")
        card1 = Image.open(str(image1_path)).convert("RGBA")
        card2 = Image.open(str(image2_path)).convert("RGBA")

        bg_width, bg_height = bg_image.size
        output = Image.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))

        new_size1 = (274, 405)
        new_image1 = card1.resize(new_size1)

        new_size2 = (274, 405)
        new_image2 = card2.resize(new_size2)

        x1, y1 = data["x1"], data["y1"]
        x2, y2 = data["x2"], data["y2"]

        output.paste(bg_image, (0, 0))
        output.paste(new_image1, (x1, y1), mask=new_image1)
        output.paste(new_image2, (x2, y2), mask=new_image2)

        return output
    
    if rn == True:
        image_files = os.listdir(input_folder)
        random.shuffle(image_files)
    elif rn == False:
        image_files = sorted(os.listdir(input_folder), key=lambda x: os.path.getmtime(os.path.join(input_folder, x)))
    image_files = [f for f in image_files if f.endswith(".png")]

    if len(image_files) >= 2:
        for i in range(0, len(image_files)-1, 2):
            image1_path = os.path.join(input_folder, image_files[i])
            image2_path = os.path.join(input_folder, image_files[i+1])

            output_image = process_image(image1_path, image2_path)
            output_image_path = os.path.join(output_folder, f"{i//2}.png")
            output_image.save(output_image_path)


# dirr = os.getcwd()
# inp_path = f"{dirr}\\in_test"
# out_path = f"{dirr}\\test"
# ib = 'smol'

# slide(inp_path, out_path, ib)