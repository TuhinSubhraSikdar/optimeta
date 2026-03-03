from PyPDF2 import PdfReader
from .base_handler import BaseHandler


class PDFViewerHandler(BaseHandler):

    def process(self):
        reader = PdfReader(self.file_path)
        metadata = reader.metadata or {}

        extracted_data = {
            "title": metadata.get("/Title"),
            "author": metadata.get("/Author"),
            "description": metadata.get("/Subject"),
            "keywords": metadata.get("/Keywords"),
            "creation_date": metadata.get("/CreationDate"),
            "modification_date": metadata.get("/ModDate"),
        }

        return extracted_data