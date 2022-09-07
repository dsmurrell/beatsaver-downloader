import json
import os
import zipfile
from io import BytesIO
from time import sleep, time

import requests

with open("config.json") as f:
    config = json.load(f)

maps = []
page_maps = ["filler"]

page = 0
print("Fetching map index.", end="", flush=True)
while len(page_maps) > 0:
    sleep(1)
    r = requests.get(f"https://api.beatsaver.com/search/text/{page}", config)
    page_maps = json.loads(r.content)["docs"]
    print(".", end="", flush=True)
    for map in page_maps:
        maps.append(map)
    page += 1
print(f"\nFetched index for {len(maps)} maps\n")

output_folder = str(int(time()))
print(f"Created folder {output_folder} for maps\n")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with open(os.path.join(output_folder, "maps.json"), "w", encoding="utf-8") as f:
    json.dump(maps, f, ensure_ascii=False, indent=4)

for map in maps:
    id = map["id"]
    name = map["name"].replace("/", "-")
    downloadURL = map["versions"][0]["downloadURL"]
    print(f"Downloading map: {name}")
    r = requests.get(downloadURL)

    try:
        with zipfile.ZipFile(BytesIO(r.content)) as zip:
            zip.extractall(os.path.join(output_folder, f"{id} ({name})"))
    except Exception:
        continue

print("\nDone! Now use SideQuest to copy them to your quest")
