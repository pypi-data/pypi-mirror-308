import os
import json

CURRENT_FILE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(CURRENT_FILE, "config")

def parse_json(json_path: str):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data

DRIVER = parse_json(os.path.join(CONFIG_PATH, "download/driver.json"))

