from PIL import Image
import piexif
from datetime import datetime
import os
from .base_handler import BaseHandler


class ImageHandler(BaseHandler):

    def format_exif_date(self, dt=None):
        if not dt:
            dt = datetime.now()
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def process(self):
        image = Image.open(self.file_path)

        # Load existing EXIF data (if any)
        try:
            exif_dict = piexif.load(image.info.get("exif", b""))
        except Exception:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

        # Get metadata from form
        title = self.metadata.get("title", "")
        author = self.metadata.get("author", "")
        description = self.metadata.get("description", "")
        keywords = self.metadata.get("keywords", "")
        custom_date = self.metadata.get("custom_datetime")

        # Date formatting
        if custom_date:
            try:
                dt = datetime.strptime(custom_date, "%Y-%m-%dT%H:%M")
            except ValueError:
                dt = datetime.now()
        else:
            dt = datetime.now()

        formatted_date = self.format_exif_date(dt)

        # Insert EXIF fields
        exif_dict["0th"][piexif.ImageIFD.Artist] = author.encode("utf-8")
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode("utf-8")
        exif_dict["0th"][piexif.ImageIFD.XPTitle] = title.encode("utf-16le")
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode("utf-16le")

        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = formatted_date.encode("utf-8")
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = formatted_date.encode("utf-8")

        exif_bytes = piexif.dump(exif_dict)

        # Create output file
        base, ext = os.path.splitext(self.file_path)
        output_path = f"{base}_optimized{ext}"

        image.save(output_path, exif=exif_bytes)

        return output_path