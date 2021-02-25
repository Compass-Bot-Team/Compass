# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
from utils import exceptions
from PIL import Image, ImageFilter


def blur_processor(image_bytes):
    with Image.open(io.BytesIO(image_bytes)) as img:
        buffer = io.BytesIO()
        img.filter(ImageFilter.GaussianBlur()).save(buffer, "png")
        buffer.seek(0)
    return buffer


def rotate_processor(degree, image_bytes):
    with Image.open(io.BytesIO(image_bytes)) as img:
        buffer = io.BytesIO()
        img.rotate(int(degree)).save(buffer, "png")
        buffer.seek(0)
    return buffer


def enlarge_processor(image_bytes):
    with Image.open(io.BytesIO(image_bytes)) as img:
        buffer = io.BytesIO()
        width, height = img.size
        if width > 5000 or height > 5000:
            raise exceptions.ImageExceedsLimit("This image's height or width is too large.")
        else:
            img.resize((round(width * 1.25), round(height * 1.25))).save(buffer, "png")
            buffer.seek(0)
    return buffer
