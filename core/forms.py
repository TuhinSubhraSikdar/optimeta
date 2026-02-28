from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField()
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)
    description = forms.CharField(required=False)
    keywords = forms.CharField(required=False)
    custom_datetime = forms.CharField(required=False)