import json
import copy
import random
import requests
import cv2
from PIL import Image
import numpy as np
import base64
from PIL import Image
from io import BytesIO

with open("./assets/templates/paparazzi_api.json", 'r') as json_file:
    template = json.load(json_file)


def base64_to_pillow_image(base64_string):
    if base64_string.startswith("data:image/png;base64,"):
        base64_string = base64_string[len("data:image/png;base64,"):]
    image_bytes = base64.b64decode(base64_string)
    image_buffer = BytesIO(image_bytes)
    pillow_image = Image.open(image_buffer)

    return pillow_image


def modify_payload(infer_props):
    face_image = infer_props.get("face_image")
    face_image = base64_to_pillow_image(face_image)
    face_image.save("./ComfyUI/input/temp.png")
    gender = infer_props.get("gender","Man")
    seed = random.randint(1, 10000000000)
    payload = copy.deepcopy(template)
    payload["3"]["inputs"]["image"] = "temp.png"
    payload["15"]["inputs"]["seed"] = seed
    if gender.lower() in ["man", "men"]:
        payload["102"]["inputs"]["directory"] = "./ComfyUI/input/MEN"
    if gender.lower() in ["woman", "women"]:
        payload["102"]["inputs"]["directory"] = "./ComfyUI/input/WOMEN"
    return payload



