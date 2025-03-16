import json
import os
from uuid import uuid4
from PIL import Image
import jsonpickle


importDir = './import/'
exportDir = './'


class Name:
    def __init__(self, zh, en):
        self.zh = zh
        self.en = en


class Index:
    def __init__(self, uuid, name, date):
        self.uuid = uuid
        self.name = name
        self.date = date


if __name__ == '__main__':
    # get existing indexs
    indexs = []
    if os.path.exists(exportDir + '.index'):
        try:
            with open(exportDir + '.index', 'r', encoding='utf-8') as file_read:
                content_read = file_read.read()
                if content_read:
                    indexs = jsonpickle.decode(content_read)
        except Exception as e:
            print("Unable to read index file")
        finally:
            file_read.close()

    total_mdx_files = 0
    error = 0

    for file in os.listdir(importDir):
        if file.endswith('.webp'):
            total_mdx_files += 1
            image = Image.open(importDir + file)

            uuid = str(uuid4())

            dateWithName = file.split('.')[0]
            date = dateWithName.split('_')[0]
            title = dateWithName.split('_')[1]

            image.save(exportDir + uuid + '.webp')
            indexs.append(Index(uuid, Name(title, title), date))
            image.close()

    # overrite the .index file
    try:
        with open(exportDir + '.index', 'w', encoding='utf-8') as file_write:
            file_write.write(jsonpickle.encode(indexs))
    except Exception as e:
        print("Unable to write index file")
    finally:
        file_write.close()

    print("Total .webp files: " + str(total_mdx_files))
    print("Error: " + str(error))
