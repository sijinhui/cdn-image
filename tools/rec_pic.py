import requests
import json
import pathlib
from tqdm import tqdm
from aip import AipImageClassify
from concurrent.futures import ThreadPoolExecutor, as_completed

""" 你的 APPID AK SK """
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''


client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def process_image(img_path):
    json_f = img_path.with_suffix(".json")
    if json_f.exists():
        return
    image = get_file_content(img_path)
    rec_result = client.advancedGeneral(image)
    with json_f.open("w", encoding='utf-8') as f:
        json.dump(rec_result, f, ensure_ascii=False)

def main(root_dir):
    img_l: [pathlib.Path] = []
    for _ in root_dir.rglob("*"):
        if _.is_file() and _.suffix != ".json":
            img_l.append(_)
    print(img_l)
    # # for img_path in tqdm(img_l):
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     futures = {executor.submit(process_image, img_path): img_path for img_path in img_l}
    #     for future in tqdm(as_completed(futures), total=len(futures)):
    #         img_path = futures[future]
    #         try:
    #             future.result()
    #         except Exception as e:
    #             print(f"Error processing {img_path}: {e}")


if __name__ == '__main__':
    root_dir = pathlib.Path(__file__).resolve().parent.parent / "api/images"



    main(root_dir)
