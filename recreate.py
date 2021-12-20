import json, os
from PIL import Image

def checkDirs():
    for dir in [
        "updatedPng",
        "updatedJpg",
        "updatedMetadata",
    ]:
        if not os.path.exists(dir):
            os.makedirs(dir)


def findFilesAndWriteNewMetaData(name):
    files = {}
    with open(f"metadata/{name}.json") as file:
        data = json.load(file)
    for att in data["attributes"]:
        trait = att["trait_type"]
        value = att["value"]

        files[trait] = f"layers/{trait}/{value}.png"
    with open(f"updatedMetadata/{name}.json", "w") as file:
        json.dump(data, file)
    return files


def processCreature(name):
  files = findFilesAndWriteNewMetaData(name)
  if name == 6129:
    files["Eyes"] = "layers/Eyes/X_Ray.png"
  holder = files.get("Eyes")
  files["Eyes"] = files.get("Chain")
  files["Chain"] = holder
  if not files:
      return
  lastImage = None
  for trait in files:
      file = files.get(trait)
      if file:
          with Image.open(file).convert("RGBA") as image:
              lastImage = (
                  Image.alpha_composite(lastImage, image) if lastImage else image
              )
  if lastImage:
      lastImage.save(f"updatedPng/{name}.png")
      with Image.open(f"updatedPng/{name}.png").convert("RGB") as image:
          image.save(f"updatedJpg/{name}.jpg")


def process():
  for i in range(1511,10000):
    # need to manually add meta and gif
    if i == 9410: 
      return
    processCreature(i)

checkDirs()
process()
