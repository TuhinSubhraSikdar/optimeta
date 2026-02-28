from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
from .forms import FileUploadForm
from .handlers.pdf_handler import PDFHandler
import os


def home(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES["file"]

            # Save uploaded file
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Collect metadata from form
            metadata_data = {
                "title": form.cleaned_data.get("title"),
                "author": form.cleaned_data.get("author"),
                "description": form.cleaned_data.get("description"),
                "keywords": form.cleaned_data.get("keywords"),
                "custom_datetime": request.POST.get("custom_datetime"),
            }

            # Use PDF Handler
            handler = PDFHandler(file_path, metadata_data)
            output_path = handler.process()

            return FileResponse(open(output_path, "rb"), as_attachment=True)

    else:
        form = FileUploadForm()

    return render(request, "core/home.html", {"form": form})