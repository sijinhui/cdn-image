import pathlib
import json
root_dir = pathlib.Path(__file__).resolve().parent.parent / "api/images"
print(root_dir)

dongman_list = []
people_list = []
for j in root_dir.rglob("*.json"):
    with j.open("r", encoding="utf-8") as f:
        t_f = f.read()
    f_name = j.with_suffix(".jpg")
    if not f_name.exists():
        print('error', f_name)
    if "动漫" in t_f:
        dongman_list.append(f_name.name + '\n')
    else:
        people_list.append(f_name.name + '\n')

with open("dongman.txt", "w", encoding='utf-8') as f:
    f.writelines(dongman_list)
with open("people_list.txt", "w", encoding='utf-8') as f:
    f.writelines(people_list)