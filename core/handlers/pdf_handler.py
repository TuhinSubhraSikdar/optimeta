from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime
import os
from .base_handler import BaseHandler


class PDFHandler(BaseHandler):

    def format_pdf_date(self, dt=None):
        if not dt:
            dt = datetime.now()
        return "D:" + dt.strftime("%Y%m%d%H%M%S")

    def process(self):
        reader = PdfReader(self.file_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        existing_metadata = reader.metadata or {}

        metadata = {
            "/Title": self.metadata.get("title") or existing_metadata.get("/Title", ""),
            "/Author": self.metadata.get("author") or existing_metadata.get("/Author", ""),
            "/Keywords": self.metadata.get("keywords") or existing_metadata.get("/Keywords", ""),
            "/Subject": self.metadata.get("description") or existing_metadata.get("/Subject", ""),
        }

        custom_date = self.metadata.get("custom_datetime")

        if custom_date:
            try:
                dt = datetime.strptime(custom_date, "%Y-%m-%dT%H:%M")
            except ValueError:
                dt = datetime.now()
        else:
            dt = datetime.now()

        metadata["/CreationDate"] = self.format_pdf_date(dt)
        metadata["/ModDate"] = self.format_pdf_date(dt)

        writer.add_metadata(metadata)

        output_path = self.file_path.replace(".pdf", "_optimized.pdf")

        with open(output_path, "wb") as f:
            writer.write(f)

        return output_path