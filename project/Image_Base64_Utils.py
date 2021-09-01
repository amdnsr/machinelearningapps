import base64
from io import BytesIO
import os
from PIL import Image

class Image_Base64_Utils:
    """
    # https://jdhao.github.io/2020/03/17/base64_opencv_pil_image_conversion/
    """
    @staticmethod
    def decode_base64_text(imageb64):
        image_bytes = base64.b64decode(imageb64)
        image_file_object = BytesIO(image_bytes)
        image_PIL_file = Image.open(image_file_object)
        return image_PIL_file

    @staticmethod
    def decode_base64_file(base64_path):
        with open(base64_path, "r") as f:
            imageb64 = f.read()
        image_PIL_file = Image_Base64_Utils.decode_base64_text(imageb64)
        return image_PIL_file
    
    @staticmethod
    def decode_base64_and_save(imageb64, input_path):
        image_PIL_file = Image_Base64_Utils.decode_base64_text(imageb64)
        image_PIL_file.save(input_path)

    @staticmethod
    def base64_file_to_image_file(base64_path, image_path):
        with open(base64_path, "r") as f:
            imageb64 = f.read()
        Image_Base64_Utils.decode_base64_and_save(imageb64, image_path)

    @staticmethod
    def encode_image_PIL_file(image_PIL_file):
        print(type(image_PIL_file), "line37")
        image_file_object = BytesIO()
        image_PIL_file.save(image_file_object, format="JPEG")
        image_bytes = image_file_object.getvalue()
        imageb64 = base64.b64encode(image_bytes)
        return imageb64

    @staticmethod
    def encode_image_file(image_path):
        image_PIL_file = Image.open(image_path)
        imageb64 = Image_Base64_Utils.encode_image_PIL_file(image_PIL_file)
        return imageb64

    @staticmethod
    def encode_image_and_save(image_PIL_file, output_path):
        print(type(image_PIL_file), "line52")
        imageb64 = Image_Base64_Utils.encode_image_PIL_file(image_PIL_file)
        print(type(imageb64), "54")
        with open(output_path, "w") as f:
            imageb64 = f.write(imageb64.decode('utf-8'))

    @staticmethod
    def image_file_to_base64_file(image_path, base64_path):
        image_PIL_file = Image.open(image_path)
        Image_Base64_Utils.encode_image_and_save(image_PIL_file, base64_path)

if __name__ == "__main__":
    input_image_path = "../HOME_DIR/input.png"
    input_base64_path = "../HOME_DIR/input.txt"

    Image_Base64_Utils.image_file_to_base64_file(input_image_path, input_base64_path)
