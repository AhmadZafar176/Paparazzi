import os
from PIL import Image
from io import BytesIO
import json
import boto3

def upload_images_to_s3(directory_path, infer_props):
    """
    Uploads all images from a directory to an S3 bucket and returns the folder link.

    :param directory_path: Path to the local directory containing images.
    :param infer_props: Dictionary containing properties such as 'uuid'.
    :return: URL to the folder where images are uploaded.
    """
    bucket_name = 'paparazzibrv'
    access_key_id = 'AKIAWHCDS3LVAGM4NP47'
    secret_access_key = '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'
    s3_client = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    uuid = infer_props["uuid"]
    s3_folder = f"{uuid}/images/"
    
    # Loop through all files in the directory
    for idx, filename in enumerate(os.listdir(directory_path)):
        # Full file path
        file_path = os.path.join(directory_path, filename)

        # Check if the file is an image by extension
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                # Open the image file
                with Image.open(file_path) as image:
                    object_key = f"{s3_folder}{uuid}_{idx}.png"

                    # Convert image to bytes for uploading
                    with BytesIO() as buffer:
                        image.save(buffer, format="PNG")
                        buffer.seek(0)
                        image_bytes = buffer.read()

                    # Upload image to S3
                    s3_client.put_object(Body=image_bytes, Bucket=bucket_name, Key=object_key)

                    print(f"Image {idx + 1} uploaded successfully to S3: {object_key}")
            except Exception as e:
                print(f"Error uploading {filename} to S3: {e}")
        else:
            print(f"Skipping non-image file: {filename}")

    # Return the link to the folder where images are uploaded
    s3_folder_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_folder}"
    return s3_folder_url


# Example usage:
# infer_props = {"uuid": "your-unique-uuid"}
# folder_url = upload_images_to_s3('/path/to/your/images/directory', infer_props)
# print("Images uploaded to:", folder_url)
