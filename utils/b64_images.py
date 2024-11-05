from PIL import Image
import io
import base64

def get_b64_response(image_list):
    base64_images = {}
    for i, image in enumerate(image_list):
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        base64_image = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
        base64_images[f"{i + 1}"] = base64_image
    return base64_images
