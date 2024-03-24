import secrets
import os
from PIL import Image
from app import app




def save_profile_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_pic.filename)
    pic_name = random_hex + file_extension
    pic_path = os.path.join(app.root_path, 'static/pics', pic_name)
    pic_size = (125, 125)
    pic = Image.open(form_pic)
    pic.thumbnail(pic_size)
    pic.save(pic_path)
    return pic_name