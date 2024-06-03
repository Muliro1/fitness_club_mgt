import secrets
import os
from PIL import Image
from app import app




def save_profile_picture(form_pic):
    """
    Resizes the image to a square of size 125x125 and saves it in the static/pics/
    directory. Returns the name of the saved image.

    Args:
        form_pic (FileStorage): The image file to be saved.

    Returns:
        str: The name of the saved image.
    """

    # Generate a random filename to prevent duplicate filenames and to secure
    # the file from being overwritten.
    random_hex = secrets.token_hex(8)

    # Get the file extension of the image.
    _, file_extension = os.path.splitext(form_pic.filename)

    # Generate a new filename by appending the random hex to the file extension.
    pic_name = random_hex + file_extension

    # Construct the path of the image to be saved.
    pic_path = os.path.join(app.root_path, 'static/pics', pic_name)

    # Set the size of the resized image.
    pic_size = (125, 125)

    # Open the image file from the form.
    pic = Image.open(form_pic)

    # Resize the image.
    pic.thumbnail(pic_size)

    # Save the resized image to the specified path.
    pic.save(pic_path)

    # Return the filename of the saved image.
    return pic_name
