import os
from PIL import Image
import random
import json

def slide(inp, outp, bg):
    input_folder = inp
    output_folder = outp

    json_file_path = os.path.join("bgs", f"{bg}.json")
    with open(json_file_path, "r") as f:
        data = json.load(f)

    cc_info_json = os.path.join(input_folder, "data.json")
    with open(cc_info_json, "r") as f:
        cc_data = json.load(f)

    if "svs" in cc_data:
        inp2 = cc_data["svs"]
    else:
        inp2 = None

    def process_image(image1_path, image2_path):
        bg_image = Image.open(data["name"]).convert("RGBA")
        card1 = Image.open(str(image1_path)).convert("RGBA")
        card2 = Image.open(str(image2_path)).convert("RGBA")

        bg_width, bg_height = bg_image.size
        output = Image.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))
        
        if "2v2" in cc_data:
            cc_size = (548, 405)
        else:
            cc_size = (274, 405)
    
        new_image1 = card1.resize(cc_size)
        new_image2 = card2.resize(cc_size)

        x1, y1 = data["x1"], data["y1"]
        x2, y2 = data["x2"], data["y2"]

        output.paste(bg_image, (0, 0))
        output.paste(new_image1, (x1, y1), mask=new_image1)
        output.paste(new_image2, (x2, y2), mask=new_image2)

        return output
    
    if "rng" in cc_data:
        image_files = sorted(os.listdir(input_folder), key=lambda x: os.path.getmtime(os.path.join(input_folder, x)))
        if inp2 is not None:
            image2_files = sorted(os.listdir(inp2), key=lambda x: os.path.getmtime(os.path.join(inp2, x)))
    else:
        image_files = os.listdir(input_folder)
        random.shuffle(image_files)
        if inp2 is not None:
            image2_files = os.listdir(inp2)
            random.shuffle(image2_files)
    image_files = [f for f in image_files if f.endswith(".png")]
    if inp2 is not None:
        print(image2_files)
        image2_files = [f for f in image2_files if f.endswith(".png")]

    if inp2 is not None:
        if len(image_files)+len(image2_files) >= 2:
            for i in range(len(image_files)):
                image1_path = os.path.join(input_folder, image_files[i])
                image2_path = os.path.join(inp2, image2_files[i])

                output_image = process_image(image1_path, image2_path)
                output_image_path = os.path.join(output_folder, f"{i}_{str(image_files[i][:-4])}-{str(image2_files[i][:-4])}.png")
                output_image.save(output_image_path)
    else:
        im_count = 0
        if len(image_files) >= 2:
            for i in range(0, len(image_files)-1, 2):
                image1_path = os.path.join(input_folder, image_files[i])
                image2_path = os.path.join(input_folder, image_files[i+1])

                output_image = process_image(image1_path, image2_path)
                output_image_path = os.path.join(output_folder, f"{im_count}_{str(image_files[i][:-4])}-{str(image_files[i+1][:-4])}.png")
                output_image.save(output_image_path)
                im_count += 1
