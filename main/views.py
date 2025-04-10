from django.shortcuts import render
from django.http import HttpResponse, FileResponse

from main.utils import download_file


def home(request):
    return HttpResponse("Hello, this is the NASWeb home page!")

def test(request):
    return HttpResponse("Hello")

def download_file_view(request, filename, download_dir):
    file_path = ''
    local_path = download_file(file_path, filename, download_dir)
    return FileResponse(open(local_path, 'rb'), as_attachment=True)
