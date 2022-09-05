import json
import bz2
import os

from pathlib import Path
import re

filePaths = ['../probesData/20220824.json.bz2', '../probesData/20170824.json.bz2']

for filePath in filePaths :

    path = Path(__file__).parent / str(filePath)

    with bz2.open(path, "r") as bzinput:
        
        tweets = json.loads(bzinput.read())
        
        my_path = str(Path(__file__).parent) # Figures out the absolute path for you in case your working directory moves around.

        my_path += '\\' + filePath[:-4].replace('/', '\\')

        with open(my_path, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, ensure_ascii=False, indent=4)