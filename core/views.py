from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
from .forms import FileUploadForm
from .handlers.pdf_handler import PDFHandler
from .handlers.image_handler import ImageHandler
from .handlers.pdf_viewer_handler import PDFViewerHandler
from .handlers.image_viewer_handler import ImageViewerHandler
import os


def home(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES["file"]

            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            metadata_data = {
                "title": form.cleaned_data.get("title"),
                "author": form.cleaned_data.get("author"),
                "description": form.cleaned_data.get("description"),
                "keywords": form.cleaned_data.get("keywords"),
                "custom_datetime": request.POST.get("custom_datetime"),
            }

            file_extension = os.path.splitext(uploaded_file.name)[1].lower()

            if file_extension == ".pdf":
                handler = PDFHandler(file_path, metadata_data)

            elif file_extension in [".jpg", ".jpeg", ".png", ".webp"]:
                handler = ImageHandler(file_path, metadata_data)

            else:
                os.remove(file_path)
                return render(request, "core/home.html", {
                    "form": form,
                    "error": "Unsupported file type."
                })

            output_path = handler.process()

            # Store file info in session
            request.session["optimized_file_path"] = output_path
            request.session["original_filename"] = uploaded_file.name

            return render(request, "core/rename_file.html", {
                "original_name": uploaded_file.name
            })

    else:
        form = FileUploadForm()

    return render(request, "core/home.html", {"form": form})


def meta_viewer(request):
    metadata = None

    if request.method == "POST":
        uploaded_file = request.FILES.get("file")

        if uploaded_file:
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            file_extension = os.path.splitext(uploaded_file.name)[1].lower()

            if file_extension == ".pdf":
                handler = PDFViewerHandler(file_path, {})

            elif file_extension in [".jpg", ".jpeg", ".png", ".webp"]:
                handler = ImageViewerHandler(file_path, {})

            else:
                os.remove(file_path)
                return render(request, "core/meta_viewer.html", {
                    "error": "Unsupported file type."
                })

            metadata = handler.process()

            # Clean up uploaded file after reading
            os.remove(file_path)

    return render(request, "core/meta_viewer.html", {
        "metadata": metadata
    })

def download_file(request):
    import re
    from django.http import HttpResponse

    file_path = request.session.get("optimized_file_path")
    original_name = request.session.get("original_filename")

    if not file_path or not os.path.exists(file_path):
        return render(request, "core/home.html", {
            "error": "File not found."
        })

    new_name = request.POST.get("new_filename")
    extension = os.path.splitext(original_name)[1]

    if new_name:
        # Convert to lowercase
        new_name = new_name.lower()

        # Replace spaces with hyphens
        new_name = new_name.replace(" ", "-")

        # Remove special characters (keep letters, numbers, hyphen)
        new_name = re.sub(r"[^a-z0-9\-]", "", new_name)

        # Remove multiple hyphens
        new_name = re.sub(r"-+", "-", new_name).strip("-")

        download_name = new_name + extension
    else:
        download_name = original_name

    # Read file content into memory
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Delete file AFTER closing it
    os.remove(file_path)

    # Clear session
    request.session.pop("optimized_file_path", None)
    request.session.pop("original_filename", None)

    response = HttpResponse(file_data, content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="{download_name}"'

    return response