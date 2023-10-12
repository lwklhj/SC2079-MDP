import os
from PIL import Image


def collate_images(path):
    images = []
    total_height = 0
    max_width = 0
    print("inside image_join")
    print(os.listdir(path))
    for f in os.listdir(path):
        if f.startswith("."):
            continue
        fol_path = os.path.join(path,f)
        print(fol_path)
        for filename in os.listdir(fol_path):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                img = Image.open(os.path.join(fol_path, filename))
                images.append(img)
                max_width = max(max_width, img.width)
                total_height += img.height

    result_image = Image.new("RGB", (int(max_width*2), int(total_height/2)), (255, 255, 255))
    y_offset = 0
    img_c = 0
    for img in images:
        if img_c % 2 == 0:
            result_image.paste(img, (0, y_offset))
        elif img_c % 2 == 1:
            result_image.paste(img, (max_width, y_offset))
            y_offset += img.height
        img_c += 1

    result_image.save(os.path.join(path, "final_image.jpg"))