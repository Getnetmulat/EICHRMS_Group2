import secrets, os
from PIL import Image
from App import app

""" Class uploading any file type to file cv in static"""
class UploadFile(object):

        # Render the file
    def save_file(form_file):
        random_hex = secrets.token_hex(8)
        _,f_ext = os.path.splitext(form_file.filename)
        file_fn = random_hex + f_ext
        file_path = os.path.join(app.root_path, 'static/attachement', file_fn)
        #output_size = (125, 125)
        #i = Image.open(form_picture)
        #i.thumbnail(output_size)
        form_file.save(file_path)
        return file_fn
    # Render the pictures
    def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        _,f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/photo', picture_fn)
        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        return picture_fn
