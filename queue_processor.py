import queue
import threading
import time
from typing import Dict
import requests
import copy
import traceback
import json
import os
import glob
from payload import modify_payload
from utils.utilss import upload_images_to_s3
import utils.api_gate as api_gate
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO

class QueueProcessor:

    def process_request(self, infer_props):
        payload = modify_payload(infer_props)
        start_time = time.time()
        images = api_gate.generate(payload)
        # Paths
        frame_path = "./ComfyUI/input/PAPARAZZAI_WATERMARKLOGO (1).png"
        images_folder = "./ComfyUI/output"  # Folder containing your 40 images
        output_folder = "./Generations"       # Folder to save the images with frames

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Load the frame image
        frame = Image.open(frame_path)

        # Process each image in the folder
        for image_file in os.listdir(images_folder):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                # Load the current image
                img_path = os.path.join(images_folder, image_file)
                img = Image.open(img_path)

                # Resize the frame to match the size of the image
                resized_frame = frame.resize(img.size)

                # Combine the image and the frame
                img_with_frame = Image.alpha_composite(img.convert("RGBA"), resized_frame.convert("RGBA"))

                # Save the resulting image
                output_path = os.path.join(output_folder, f"framed_{image_file}")
                img_with_frame.save(output_path, format="PNG")
                print(f"Processed and saved: {output_path}")
        folder_link = upload_images_to_s3("./Generations/",infer_props)
        for file_path in glob.glob(os.path.join('./ComfyUI/output/', '*.png')):
            os.remove(file_path)
        for file_path in glob.glob(os.path.join('./Generations/', '*.png')):
            os.remove(file_path)

        output = {
            "images": folder_link
        }


        response = {
            "response": output
        }

        return response
