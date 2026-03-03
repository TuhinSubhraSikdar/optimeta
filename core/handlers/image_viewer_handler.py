from PIL import Image
import piexif
from .base_handler import BaseHandler


class ImageViewerHandler(BaseHandler):

    def process(self):
        image = Image.open(self.file_path)

        try:
            exif_dict = piexif.load(image.info.get("exif", b""))
        except Exception:
            exif_dict = {}

        def decode(value, encoding="utf-8"):
            try:
                return value.decode(encoding)
            except Exception:
                return None

        extracted_data = {
            "title": decode(exif_dict.get("0th", {}).get(piexif.ImageIFD.XPTitle, b""), "utf-16le"),
            "author": decode(exif_dict.get("0th", {}).get(piexif.ImageIFD.Artist, b"")),
            "description": decode(exif_dict.get("0th", {}).get(piexif.ImageIFD.ImageDescription, b"")),
            "keywords": decode(exif_dict.get("0th", {}).get(piexif.ImageIFD.XPKeywords, b""), "utf-16le"),
            "creation_date": decode(exif_dict.get("Exif", {}).get(piexif.ExifIFD.DateTimeOriginal, b"")),
            "modification_date": decode(exif_dict.get("Exif", {}).get(piexif.ExifIFD.DateTimeDigitized, b"")),
        }

        return extracted_data