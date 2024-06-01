import json
import os
import pathlib
from PIL import Image
from tqdm import tqdm

def get_img_h_w(file_path):
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            if width >= height:
                return "pc"
            else:
                return "mobile"
    except Exception as e:
        print(f'Skipping {file_path}, not an image file.')

def get_img_lx(file_path):
    json_info = file_path.with_suffix(".json")
    if not json_info.exists():
        print("json error", json_info)
    with json_info.open("r", encoding="utf-8") as f:
        json_data = f.read()
    if ("风景" in json_data or "自然" in json_data or "植物" in json_data) and "美女" not in json_data:
        return "fengjing"
    if "动漫" in json_data:
        return "dongman"
    return "meizi"

def move_images_based_on_orientation(src_folder, horizontal_folder, vertical_folder):
    os.makedirs(horizontal_folder, exist_ok=True)
    os.makedirs(vertical_folder, exist_ok=True)

    for filename in tqdm(os.listdir(src_folder)):
        file_path = src_folder / filename
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                if width >= height:
                    new_path = horizontal_folder / filename
                else:
                    new_path = vertical_folder / filename
            os.rename(file_path, new_path)
        except Exception as e:
            print(f'Skipping {filename}, not an image file.')

def main(root_dir):
    img_l: [pathlib.Path] = []
    for _ in root_dir.rglob("*"):
        if _.is_file() and _.suffix != ".json":
            img_l.append({
                "name": _.name,
                "lx": get_img_lx(_),
                "method": get_img_h_w(_),
                "imgurl": f"/{_.relative_to(root_dir.parent.parent).as_posix()}",
            })

    with open(root_dir.parent.parent / "img_url.json", "w", encoding='utf-8') as f:
        json.dump(img_l, f, ensure_ascii=False,)


if __name__ == '__main__':
    root_folder = pathlib.Path(__file__).resolve().parent.parent / "api/images"

    main(root_folder)